
# MKV 與 SRT 合併並翻譯工具

這是一個使用 `ffmpeg` 和 `Python` 的 GUI 專案，它可以合併 `.mkv` 檔案和 `.srt` 檔案。同時，它會將 `.srt` 檔案中的簡體中文翻譯成繁體中文 (zh-TW)。

## 系統需求

- Python 3.8
- ffmpeg

## 安裝

1. 安裝必要的 Python 套件:

```bash
pip install -r requirements.txt
```

2. 確保 `ffmpeg` 已安裝在您的系統上。

## 使用方式

1. 運行 `mergeSubtitles.py` 啟動 GUI。
2. 選擇您的 `.mkv` 和 `.srt` 檔案。
3. 選擇輸出的目錄和檔名。
4. 點擊 "Merge" 進行合併。

## 貢獻

如果您對這個專案有任何建議或想要貢獻，歡迎提交 Pull Request。
