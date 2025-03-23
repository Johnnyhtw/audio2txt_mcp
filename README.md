# 音訊轉文字 MCP 服務

這是一個使用 Whisper 將會議錄音檔轉換為文字的 MCP 服務。它可以與 CLINE 一起使用，讓 CLINE 能夠使用 Ollama 的本地 AI 模型來生成會議摘要。

## 功能

- 使用 OpenAI 的 Whisper 模型將音訊檔案轉換為文字
- 自動將轉錄的文字保存在與音訊檔案相同的路徑下
- 通過 MCP 協議與 CLINE 整合

## 安裝

1. 確保您已安裝 Python 3.8 或更高版本
2. 確保本機有安裝Whisper
```bash
pip install git+https://github.com/openai/whisper.git
```
3. 依據你的平台安裝ffmpeg
4. 安裝依賴項：

```bash
pip install -r requirements.txt
```

## 配置 CLINE

要在 CLINE 中使用此 MCP 服務，您需要在 CLINE 的 MCP 設定檔中添加以下配置：

```json
{
  "mcpServers": {
    "audio-transcription": {
      "command": "python",
      "args": ["完整路徑/audio_transcription_server.py"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

請將 `完整路徑` 替換為此項目的實際路徑。

## 使用方法

一旦配置完成，您可以在 CLINE 中使用此服務：

1. 在 CLINE 中，您可以使用 `audio-transcription` 服務的 `transcribe_audio` 工具
2. 提供音訊檔案的完整路徑作為參數
3. 服務將返回轉錄的文字，並在音訊檔案的位置保存一個 .txt 文件
4. 然後，您可以使用CLINE在Act模式下來生成會議摘要

## 範例

在 CLINE Act模式中透過Prompt來進行測試，下面的Prompt提供您參考：

```
幫我將這段錄音檔：C:/path/to/meeting.m4a 生成摘要
```

## 注意事項

- 第一次運行時，Whisper 會下載模型，這可能需要一些時間
- 支持的音訊格式包括 m4a、mp3、wav 等
- 轉錄大型音訊檔案可能需要較長時間，取決於您的硬體性能
- 如果您的電腦有 GPU，Whisper 會自動使用它來加速處理
