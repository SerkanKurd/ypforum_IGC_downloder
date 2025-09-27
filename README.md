<h1>Bu repo https://www.ypforum.com/leonardo sitesinden IGC dosyalarını kolayca indirmek için hazırlanmıştır.</h1>
<br>
<br>


<img width="558" height="531" alt="Screenshot 2025-09-27 at 08 48 04" src="https://github.com/user-attachments/assets/e2a0c0f8-1f76-4b4b-b00f-54318c632863" />

<br>
<br>
<h2>Build Docker Container</h2>
<code>docker build -t igcdownloader .</code>
<br><code>docker tag igcdownloader:latest igcdownloader:latest</code>
<br><code>docker run -d --name igcdownloader -p 8000:8000 igcdownloader:latest</code>
<br>
<br>
<h2>Using PreBuilt Docker Container</h2>
<code>docker run -d --name igcdownloader -p 8000:8000 serkankurd/igcdownloader:latest</code>
