# 資訊安全管理課程筆記

以課堂教材為基礎的個人複習網站，目前收錄資安三要素、數位簽章與資產風險評估。首頁依主題分組，支援關鍵字搜尋。每篇筆記都有重點摘要、概念說明、例子或應用和來源。

## 本機閱讀

使用瀏覽器開啟 [index.html](index.html)。首頁、搜尋與筆記頁都能直接使用相對路徑，無需啟動伺服器。

## GitHub Pages

1. 建立 GitHub repository，將此資料夾**裡的檔案**上傳到預定發布分支的最外層，包含 `.nojekyll`。在 repository 的檔案列表應能直接看到 `index.html` 和 `AGENTS.md`。
2. 到 **Settings → Pages**，在 **Source** 選 **Deploy from a branch**，選已上傳的分支（通常是 `main`）與 **/(root)**，再儲存。
3. 發布後從 Pages 設定複製實際網址。用該網址開啟首頁，測試搜尋、進入筆記和返回目錄。

[GitHub Pages 官方設定說明](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 延伸方式

請 AI 先讀 [AGENTS.md](AGENTS.md)，再依既有筆記的格式新增一個 Markdown 檔。執行 `python build.py`，首頁自動按分類收錄，並產生同樣版型的筆記頁。新增分類只需設定分類欄位。Python 3.9 以上即可重新產生網頁，部署可直接使用已附的 HTML。


