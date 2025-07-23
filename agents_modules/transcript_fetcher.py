from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable
import time
import random

def fetch_transcripts(video_ids: list[str]) -> list[dict]:
    """
    Fetches transcripts for a list of YouTube video IDs.
    
    Args:
        video_ids (list[str]): List of YouTube video IDs.
        
    Returns:
        list[dict]: List of dictionaries with id, title, transcript_text.
    """
    results = []
    
    for vid in video_ids:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(vid)
            transcript_text = " ".join([entry["text"] for entry in transcript_list])
            
            results.append({
                "id": vid,
                "title": f"Video {vid}",
                "transcript": transcript_text
            })


        except (TranscriptsDisabled, VideoUnavailable, Exception) as e:
            print(f"Skipping {vid}: {e}")
            continue

        time.sleep(random.uniform(1.5, 2.5))

    
    return results
