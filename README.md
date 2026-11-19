# 拾句 — 每日閱讀手札

繁體中文靜態閱讀 App。四種類型各 1,000 則，共 4,000 則。每天依台北日期各選 5 則，共 20 則；任意連續 200 天不重複，之後重啟循環。今日主句包含在 20 則內。

## 執行與檢查

以任一靜態 HTTP 伺服器提供 `dist/`，例如：

```sh
python3 -m http.server 8000 --directory dist
node --check dist/app.js
node tests/journal.test.cjs
```

無套件安裝或建置步驟。需透過 HTTP 開啟，讓瀏覽器可讀取 `quotes.json`。

## 內容與選句

`dist/quotes.json` 含原創觀點、古典短句、文學節選及古詩各 1,000 則。四類各自按固定順序分成 200 組，每日各選一組。主題是輔助分類，不保證每天五主題數量相同。全句庫每頁 60 則。

原創包含原有 125 則及 875 則情境化短句（35 個對話情境 × 25 項表達方法），不是古人引言。新增引用以固定版本的 chinese-poetry 語料為電子底本，按句界節錄、去重，附作品、作者、段落位置、原文範圍與同段原文。這些新增內容提供閱讀提示，不宣稱逐句人工校勘或白話翻譯。

完整來源檔案及 MIT 授權在 `sources/`，版本記錄在 `sources/provenance.json`。`python3 scripts/expand-library.py` 可從保留的語料重建句庫與 `dist/library-report.json`；舊有 140 則 ID 保留。`python3 scripts/package-offline.py` 重建獨立 HTML 及 ZIP。修改資料後須重新產生兩者，並提升 Service Worker 快取版本。

## 本機資料

收藏、心得、情境標籤、表達練習、當日閱讀進度及複習紀錄存在瀏覽器 `localStorage` 的 `shiju-v1`。既有收藏 ID 與練習會保留，選句版本改變時只重設當日閱讀進度。沒有帳號同步，清除網站資料或換瀏覽器不會保留紀錄。

測試涵蓋跨週輪替、舊資料、類型及作者搜尋、心得與標籤、文字跳脫、練習轉入、複習、閱讀進度與儲存失敗提示。使用輕量 DOM 模擬，不能替代真實瀏覽器的版面與操作檢查。

## 桌面與離線

線上版提供 Web App Manifest 與 Service Worker，首次連線完成後可使用瀏覽器安裝功能加入桌面。快取僅包含本站 App 資源；原文外部連結仍需網路。更新快取清單時須調整 `sw.js` 的快取版本。

`python3 scripts/package-offline.py` 會產生 `dist/shiju-offline.html` 和 `dist/shiju-offline.zip`。獨立 HTML 內嵌 CSS、程式與全部句庫，可以直接用 `file://` 開啟；無外部字型或程式依賴。下載版與線上版的瀏覽器儲存各自獨立。

`node tests/offline.test.cjs` 檢查獨立檔案在禁止網路時的功能，以及模擬 Service Worker 的快取與離線回應。這些檢查不代表已完成特定作業系統的安裝測試。

## 4,000 則版本驗證

```sh
python3 tests/library.test.py
node tests/journal.test.cjs
node tests/offline.test.cjs
```

涵蓋每類 1,000 則、正規化後無重複、十組跨邊界的完整 200 日輪替、舊 ID 保留、引用與保留語料一致、原文範圍及引號完整、下載 ZIP 與獨立 HTML 一致、離線資料包含 4,000 則。瀏覽器安裝與版面仍須另行實測。
