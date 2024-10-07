from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import yt_dlp
import os

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

@app.get("/video-formats")
async def list_video_formats(url: str):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            formats = info_dict.get('formats', [])
            thumbnail = info_dict.get('thumbnail')
            if not formats:
                formats = [info_dict]  
            
            available_formats = []
            for f in formats:
                resolution = f.get('resolution', None)
                ext = f.get('ext', None)
                acodec = f.get('acodec', None)
                vcodec = f.get('vcodec', None)
                
                # Filter for 480p, 720p, and 1080p with mp4 and m4a formats
                # if (resolution in ['854x480', '1280x720', '1920x1080'] ) or (ext == 'm4a' and acodec == 'mp4a.40.2'):
                available_formats.append({
                        'format_id': f.get('format_id'),
                        'resolution': resolution,
                        'ext': ext,
                        'vcodec': vcodec,
                        'acodec': acodec,
                    })
            
            return {'formats': available_formats,'thumbnail': thumbnail }
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/download")
async def download_video(url: str, format_id: str):
    try:
        ydl_opts = {
            'format': format_id,
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', None)
            output_file_path = f"{title}.mp4"

        # Return the video file
        return FileResponse(output_file_path, media_type="video/mp4", filename=output_file_path)

    except Exception as e:
        # Log the error for debugging
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
