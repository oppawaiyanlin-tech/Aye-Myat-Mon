# Love Proposal Bot + Website

## Upload GIFs
Put exactly these 9 GIF files in `static/gifs/`:
`step1.gif`, `step2.gif`, `step3.gif`, `step4.gif`, `step5.gif`, `step6.gif`, `step7.gif`, `step8.gif`, `yes.gif`.
Each click on **မချစ်ဘူး 💔** updates the text and corresponding GIF. Clicking **ချစ်တယ် ❤️** displays only the final message and `yes.gif`.

## Deploy to Render
1. Create a Telegram bot using @BotFather. Keep the token secret.
2. Upload this whole project to a GitHub repository, including the `templates/` and `static/gifs/` directories.
3. In Render, create a Python Web Service connected to your GitHub repo, or use `render.yaml` as a Blueprint.
4. Configure `BOT_TOKEN`, `ADMIN_ID` (your numeric Telegram user ID), and `PUBLIC_URL` (exact Render HTTPS service URL, without trailing slash). `WEBHOOK_SECRET` must be a strong random string (Render Blueprint generates it).
5. Deploy. Visit the `PUBLIC_URL` to see the website. Message the Telegram bot `/start` then `/link` to receive the shareable link.
6. You may customize `PAGE_TITLE` and `PAGE_MESSAGE` in Render environment settings.

**Important:** The bot sends the website link; the animated page is viewed in the browser, not as an interactive Telegram message. TikTok videos also cannot run these buttons. The final message does not submit or collect any invitation text.

GIFs are intentionally not included. Missing GIFs display broken-image placeholders until you upload them.
