"""Build a self-contained file://-capable HTML and downloadable ZIP."""
from pathlib import Path
import json,re,zipfile
root=Path(__file__).resolve().parents[1]
dist=root/'dist'
s=(dist/'index.html').read_text()
s=re.sub(r'<link[^>]+>', '', s)
s=s.replace('</head>','<style>'+(dist/'style.css').read_text()+'</style></head>')
quotes=json.loads((dist/'quotes.json').read_text())
s=s.replace('<script src="app.js"></script>','<script>globalThis.SHIJU_QUOTES='+json.dumps(quotes,ensure_ascii=False).replace('<','\\u003c')+';</script><script>'+(dist/'app.js').read_text().replace('</script','<\\/script')+'</script>')
s=s.replace('<a href="shiju-offline.zip" download>下載離線 ZIP 包</a>', '')
s=s.replace('href="./"','href="#"').replace('href="shiju-offline.html" download="拾句離線版.html"','href="#" hidden')
(dist/'shiju-offline.html').write_text(s)
readme='拾句獨立離線版\n\n解壓縮後，直接用 Chrome、Edge 或 Safari 開啟「拾句離線版.html」。不需要安裝軟體、不需要網路或登入。\n\n包含4000則句庫、四種類型各1000則，每日各選5則，200天不重複、收藏、心得、情境標籤與練習。使用裝置的台北日期計算每日選句。\n\n資料保存在開啟檔案的瀏覽器。不同瀏覽器、檔案位置或線上版不會共用資料；部分瀏覽器可能限制本機檔案儲存，儲存失敗時會顯示提示。請先試存一則收藏並重新開啟確認。\n\n換電腦或更新檔案前，請在「閱讀設定與資料備份」匯出 JSON 備份，再到新版本選擇備份檔並確認合併匯入。可調整字級、行距與夜間模式，並選擇閱讀偏好。\n\n原文出處的外部連結需要網路。\n'
with zipfile.ZipFile(dist/'shiju-offline.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('拾句離線版.html',s);z.writestr('使用說明.txt',readme);z.writestr('來源授權.txt',(root/'sources/LICENSE').read_text());z.writestr('句庫說明.json',(dist/'library-report.json').read_text())
print('Built standalone HTML and ZIP.')
