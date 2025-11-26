#!/usr/bin/env python3
import importlib.metadata
import io
import sys
import logging
from pathlib import Path
from typing_extensions import Annotated

import typer
from gpt4all import GPT4All

logging.basicConfig(
    level=logging.INFO,
    format='\n%(levelname)s: %(message)s'
)
LOGGER = logging.getLogger(__name__)
VERSION = '1.0'

CLI_START_MESSAGE = f"""
██╗███╗   ██╗████████╗███████╗██╗     ██████╗ ███████╗██████╗  ██████╗ ██████╗ ████████╗
██║████╗  ██║╚══██╔══╝██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
██║██╔██╗ ██║   ██║   █████╗  ██║     ██████╔╝█████╗  ██████╔╝██║   ██║██████╔╝   ██║   
██║██║╚██╗██║   ██║   ██╔══╝  ██║     ██╔══██╗██╔══╝  ██╔═══╝ ██║   ██║██╔══██╗   ██║   
██║██║ ╚████║   ██║   ███████╗███████╗██║  ██║███████╗██║     ╚██████╔╝██║  ██║   ██║   
╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
"""

# Default directive used when the user does not supply one.
DEFAULT_DIRECTIVE = (
    "You are an Intelligence Analyst. Read the following interview transcript and extract the most important and factual intelligence insights into bullet points. "
    "Focus on confirmed facts: key events, dates, people, locations, motivations, and implications. "
    "Formatting rules: "
    "Every sentence must be a bullet point. "
    "Do not include paragraphs, explanations, or numbered lists. "
    "Do not deviate from bullet points under any circumstances. "
)

TOKEN_CONTEXT_WINDOW = 2048
TOKENS_PER_WORD = 1.3

# create typer app
app = typer.Typer()

def _chunk_text_by_tokens(text: str, max_tokens: int) -> list[str]:
    """Split text into chunks that fit within max_tokens limit."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    for word in words:
        word_tokens = max(1, int(len(word) * TOKENS_PER_WORD))
        
        if current_token_count + word_tokens > max_tokens and current_chunk:
            # Start a new chunk
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_token_count = word_tokens
        else:
            current_chunk.append(word)
            current_token_count += word_tokens
    
    # Add the final chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def _read_transcript(transcript_file_path: str | None) -> str:
    """Read transcript from file if provided."""
    if transcript_file_path:
        try:
            with open(transcript_file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading transcript file: {e}")
            return ""
    return ""

def _read_directive(directive_file_path: str | None) -> str:
    if directive_file_path:
        try:
            with open(directive_file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return DEFAULT_DIRECTIVE
    return DEFAULT_DIRECTIVE

def _process_chunk(gpt4all_instance, directive: str, chunk: str, chunk_num: int, total_chunks: int) -> str:
    """Process a single transcript chunk and return the response."""
    message = f"{directive}\n[Begin Transcript]\n{chunk}\n[End Transcript]"
    
    LOGGER.info(f"Processing Chunk [{chunk_num}/{total_chunks}]")
    
    try:
        # Execute chat completion with streaming
        response_generator = gpt4all_instance.generate(
            message,
            # preferential kwargs for chat ux
            max_tokens=4096,  # Increased to prevent cutting off responses
            temp=0.9,
            top_k=40,
            top_p=0.9,
            min_p=0.0,
            repeat_penalty=1.1,
            repeat_last_n=64,
            n_batch=9,
            # required kwargs for cli ux (incremental response)
            streaming=True,
        )
        
        response = io.StringIO()
        for token in response_generator:
            print(token, end='', flush=True)
            response.write(token)
        
        response_text = response.getvalue()
        response.close()
        
        return response_text
    
    except Exception as e:
        LOGGER.error(f"Error processing chunk [{chunk_num}/{total_chunks}]: {str(e)}")
        return ""

def _main_loop(model: str, device: str, n_threads: int, summarize: str, transcript: str, filename: str, directive: str):
    """Process transcript or direct text input."""
    output_path = Path.cwd() / "reports" / f"{filename}.txt"
    
    # Determine the text to process
    text_to_process = ""
    if transcript:
        # Read from transcript file
        text_to_process = _read_transcript(transcript)
        if not text_to_process:
            print("No transcript content found. Using direct input instead.")
            text_to_process = summarize if summarize else ""
    else:
        # Use direct input
        text_to_process = summarize if summarize else ""
    
    if not text_to_process:
        print("No text provided to process.")
        return
    
    # Split text into chunks based on token limit
    chunks = _chunk_text_by_tokens(text_to_process, TOKEN_CONTEXT_WINDOW)
    
    LOGGER.info(f"Processing {len(chunks)} chunk(s) of transcript...")
    
    all_responses = []
    
    for idx, chunk in enumerate(chunks, 1):
        # Create a fresh GPT4All instance for each chunk
        gpt4all_instance = GPT4All(model, device=device)
        
        # Set thread count if specified
        if n_threads is not None:
            gpt4all_instance.model.set_thread_count(n_threads)
        
        response = _process_chunk(gpt4all_instance, directive, chunk, idx, len(chunks))
        all_responses.append(response)
    
    # Write all responses to file
    print(f"\n\nWriting results to {output_path}...\n")
    
    # Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "a", encoding="utf-8") as file:
        for idx, response in enumerate(all_responses, 1):
            if len(chunks) > 1:
                file.write(f"=== CHUNK {idx} ANALYSIS ===\n")
            file.write(response + "\n")
            if len(chunks) > 1:
                file.write("\n")
    
    print(f"Results saved to {output_path}")

@app.command()
def repl(
    model: Annotated[
        str,
        typer.Option("--model", "-m", help="Model to use for analysis."),
    ] = "mistral-7b-instruct-v0.1.Q4_0.gguf",
    n_threads: Annotated[
        int,
        typer.Option("--n-threads", "-t", help="Number of threads to use for analysis."),
    ] = None,
    device: Annotated[
        str,
        typer.Option("--device", "-d", help="Device to use for analysis, e.g. gpu, amd, nvidia, intel. Defaults to CPU."),
    ] = None,
    summarize: Annotated[
        str,
        typer.Option("--sum", "-s", help="String of text to summarize."),
    ] = None,
    transcript: Annotated[
        str,
        typer.Option("--transcript", "-x", help="Path to transcript file to process."),
    ] = None,
    directive_file: Annotated[
        str,
        typer.Option("--directive", "-dir", help="Path to custom directive file."),
    ] = None,
    filename: Annotated[
        str,
        typer.Option("--file", "-f", help="Name of file for output."),
    ] = None,
):
    """The CLI read-eval-print loop."""
    print(CLI_START_MESSAGE) 

    directive = _read_directive(directive_file)

    _main_loop(model, device, n_threads, summarize, transcript, filename, directive)

@app.command()
def version():
    """The CLI version command."""
    print(f"IntelReport v{VERSION}")

if __name__ == "__main__":
    app()
