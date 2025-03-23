from mcp.server.fastmcp import FastMCP
import asyncio
import os
import time
import whisper

mcp = FastMCP("Whisper 音訊轉錄工具")

@mcp.tool(name="transcribe", description="轉錄 m4a / mp3 錄音檔為文字的 Whisper 工具")
async def transcribe_audio(audio_path: str) -> dict:
    """
    使用 Whisper 將錄音檔案（如 .m4a 或 .mp3）轉換為逐字稿文字。

    參數：
        audio_path (str): 音訊檔案的完整本機路徑，例如：C:\\Users\\me\\meeting.m4a

    回傳：
        dict: 包含逐字稿文字內容與儲存路徑：{
            "text": 逐字稿內容 (str),
            "txt_file": 產生的 .txt 檔案路徑 (str)
        }
    
    此工具支援中文錄音並會自動儲存 .txt 檔案。
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"找不到檔案：{audio_path}")

    print("[Whisper] 開始加載模型...")
    start_time = time.time()
    
    # 使用 run_in_executor 在非阻塞方式下加載模型
    model = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: whisper.load_model("small")
    )
    print(f"[Whisper] 模型加載完成，耗時 {time.time() - start_time:.2f} 秒")
    
    print(f"[Whisper] 開始轉錄音訊檔案: {audio_path}")
    start_time = time.time()
    
    # 使用 run_in_executor 在非阻塞方式下進行轉錄
    result = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: model.transcribe(audio_path, language="zh")
    )
    
    transcribed_text = result["text"]
    print(f"[Whisper] 轉錄完成，耗時 {time.time() - start_time:.2f} 秒")
    
    # 保存文字檔案
    base = os.path.splitext(audio_path)[0]
    txt_path = base + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcribed_text)
    print(f"[Whisper] 文字已保存至: {txt_path}")
    
    # 顯示部分轉錄結果
    preview_length = min(200, len(transcribed_text))
    print("\n[Whisper] 轉錄結果預覽:")
    print("-" * 50)
    print(transcribed_text[:preview_length] + ("..." if len(transcribed_text) > preview_length else ""))
    print("-" * 50)
    
    text = transcribed_text

    return {"text": text, "txt_file": txt_path}

if __name__ == "__main__":
    mcp.run()
