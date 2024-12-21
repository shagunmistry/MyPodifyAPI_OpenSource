import os
import argparse
import json
from pathlib import Path
import asyncio
from datetime import datetime
from typing import List, Dict

from document_processor import analyze_document, UnsupportedFileTypeError
from logger import CustomLogger
from ai_helper.generate_outline import generate_podcast_outline
from ai_helper.script_generator import generate_podcast_script
from ai_helper.generate_speech import text_to_speech
from utils.combine_audio import combine_audio_files

# Set up logging
log = CustomLogger("PodcastGenerator", log_file="podcast_generator.log")

class PodcastGenerator:
    def __init__(self, input_dir: str, output_dir: str, project_name: str, 
                 host_count: int = 2, description: str = ""):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.project_name = project_name
        self.host_count = host_count
        self.description = description
        self.project_dir = self.output_dir / self.sanitize_filename(project_name)
        
        # Create output directories
        self.project_dir.mkdir(parents=True, exist_ok=True)
        (self.project_dir / "documents").mkdir(exist_ok=True)
        (self.project_dir / "outlines").mkdir(exist_ok=True)
        (self.project_dir / "scripts").mkdir(exist_ok=True)
        (self.project_dir / "audio").mkdir(exist_ok=True)

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Convert string to valid filename."""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).strip()

    async def process_documents(self) -> List[str]:
        """Process all documents in the input directory."""
        document_contents = []
        
        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {self.input_dir}")

        for file_path in self.input_dir.rglob('*'):
            if file_path.is_file():
                try:
                    log.log_info(f"Processing document: {file_path}")
                    content = await analyze_document(str(file_path))
                    document_contents.append(content)
                    
                    # Save processed content
                    output_path = self.project_dir / "documents" / f"{file_path.stem}_processed.txt"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                except UnsupportedFileTypeError as e:
                    log.log_error(f"Skipping unsupported file {file_path}: {str(e)}")
                except Exception as e:
                    log.log_error(f"Error processing file {file_path}: {str(e)}")

        return document_contents

    async def generate_outline(self, document_contents: List[str]) -> str:
        """Generate podcast outline from document contents."""
        log.log_info("Generating podcast outline")

        log.log_debug(document_contents[0][:100])
        
        # Combine all document contents with description
        combined_content = "\n\n".join([self.description] + document_contents)
        
        # Generate outline
        outline = await generate_podcast_outline(combined_content, self.host_count)
        
        # Save outline
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        outline_path = self.project_dir / "outlines" / f"outline_{timestamp}.md"
        with open(outline_path, 'w', encoding='utf-8') as f:
            f.write(outline)
            
        return outline

    async def generate_script(self, outline: str, document_contents: List[str]) -> str:
        """Generate podcast script from outline and document contents."""
        log.log_info("Generating podcast script")
        
        # Combine all document contents
        combined_content = "\n\n".join(document_contents)
        
        # Generate script
        script = await generate_podcast_script(outline, combined_content, self.host_count)
        
        # Save script
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_path = self.project_dir / "scripts" / f"script_{timestamp}.md"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
            
        return script
    
    async def generate_audio(self, script: str) -> str:
        """Generate audio from script."""
        log.log_info("Generating audio file")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Convert project_dir to Path if it isn't already
        project_dir = Path(self.project_dir)
        
        # Create the audio directory path
        audio_dir = project_dir / "audio"
        
        # Create the audio directory if it doesn't exist
        audio_dir.mkdir(parents=True, exist_ok=True)
        
        # Create the full audio file path
        audio_path = audio_dir / f"podcast_{timestamp}.mp3"
        
        await text_to_speech(script, str(audio_path))
        
        return str(audio_path)

    async def generate_podcast(self) -> Dict:
        """Generate complete podcast from documents."""
        try:
            # Process all documents
            document_contents = await self.process_documents()
            if not document_contents:
                raise ValueError("No valid documents found to process")
            
            log.log_info(f"Processed {len(document_contents)} documents")

            # Generate outline
            outline = await self.generate_outline(document_contents)
            
            log.log_debug(outline[:100])

            # Generate script
            script = await self.generate_script(outline, document_contents)

            # Generate audio
            audio_path = await self.generate_audio(script)

            # Get all segment files
            audio_dir = Path(self.project_dir) / "audio"
            segment_files = sorted(list(audio_dir.glob("segment_*.wav")))
            
            if not segment_files:
                raise ValueError("No audio segments found to combine")

            # Combine all the audio files into a single file
            audio_combined_path = audio_dir / "podcast_combined.mp3"
            combine_audio_files(segment_files, audio_combined_path)

            # Save project metadata
            metadata = {
                "project_name": self.project_name,
                "host_count": self.host_count,
                "description": self.description,
                "timestamp": datetime.now().isoformat(),
                "input_directory": str(self.input_dir),
                "output_directory": str(self.project_dir),
                "audio_segments": [str(f) for f in segment_files],
                "audio_combined_file": str(audio_combined_path),
            }
            
            metadata_path = Path(self.project_dir) / "metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            return metadata

        except Exception as e:
            log.log_error(f"Error generating podcast: {str(e)}")
            raise

def main():
    input_dir = 'my_docs'
    output_dir = input("Enter the output directory for generated files (default: output): ") or 'output'
    project_name = input("Enter the name of the project: ")
    host_count = input("Enter the number of podcast hosts (default: 2): ") or 2
    description = input("Enter the project description (optional): ")

    try:
        generator = PodcastGenerator(
            input_dir,
            output_dir,
            project_name,
            int(host_count),
            description
        )

        metadata = asyncio.run(generator.generate_podcast())
        log.log_info("Podcast generation completed successfully!")
        log.log_info(f"Output files are in: {metadata['output_directory']}")

    except Exception as e:
        log.log_error(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()