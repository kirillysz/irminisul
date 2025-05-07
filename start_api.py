import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.api.v1.api:root",
        reload=True,
        host="0.0.0.0",
        port=9443,
        ssl_keyfile="/etc/letsencrypt/live/appwrite.irminsul.space/privkey.pem",
        ssl_certfile="/etc/letsencrypt/live/appwrite.irminsul.space/fullchain.pem"
    )
