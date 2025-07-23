from youtubesearchpython import VideosSearch

def youtube_search(product: str, max_results: int = 10) -> list[str]:
    """
    Searches YouTube for product review videos using youtube-search-python.
    
    Args:
        product (str): Product name to search for.
        max_results (int): Number of top video results to return.
        
    Returns:
        List[str]: List of YouTube video IDs.
    """
    query = f"{product} review"
    videos_search = VideosSearch(query, limit=max_results)
    results = videos_search.result().get("result", [])
    
    video_ids = []
    for video in results:
        link = video.get("link", "")
        if "watch?v=" in link:
            video_id = link.split("watch?v=")[-1]
            video_ids.append(video_id)
    
    return video_ids
