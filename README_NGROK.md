# Hosting Aorbo Treks Website with Ngrok

This guide explains how to host your Aorbo Treks Django website using ngrok for temporary public access.

## Prerequisites

1. Install ngrok from [https://ngrok.com/download](https://ngrok.com/download)
2. Sign up for a free ngrok account and get your authtoken
3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Setting Up Ngrok

1. After installing ngrok, authenticate with your authtoken:
   ```
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

## Running the Website with Ngrok

### Option 1: Using the Automated Script

1. Simply run the batch file:
   ```
   start_ngrok.bat
   ```
   
   Or run the Python script directly:
   ```
   python start_with_ngrok.py
   ```

2. The script will:
   - Start the Django development server
   - Start ngrok and create a tunnel to your local server
   - Open your website in the default web browser
   - Display the public ngrok URL that you can share with others

### Option 2: Manual Setup

1. Start your Django server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

2. In a separate terminal, start ngrok:
   ```
   ngrok http 8000
   ```

3. Look for the forwarding URL in the ngrok terminal (e.g., `https://abc123.ngrok-free.app`)

4. Access your website using this URL

## Important Notes

- The ngrok URL will change each time you restart ngrok unless you have a paid plan
- The free tier of ngrok has limitations on connection time and bandwidth
- For production use, consider a proper hosting service like Heroku, AWS, or DigitalOcean

## Troubleshooting

If you encounter issues with CSRF validation or other security features:

1. Make sure your Django settings are properly configured for ngrok (already done in this project)
2. Check that the `CSRF_TRUSTED_ORIGINS` setting includes your ngrok domain
3. Verify that the `NgrokProxyMiddleware` is in your middleware list

## Additional Resources

- [Ngrok Documentation](https://ngrok.com/docs)
- [Django Documentation](https://docs.djangoproject.com/)
