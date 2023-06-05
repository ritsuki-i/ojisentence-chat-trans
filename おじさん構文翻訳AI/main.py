import os
import openai
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import Annotated
import shutil

openai.api_key = "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"


def get_completion_trans(prompt, model="gpt-3.5-turbo", temperature=0):
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=
    temperature,  # this is the degree of randomness of the model's output
  )
  return response.choices[0].message["content"]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
  return {"message": "Hello World"}


class Item(BaseModel):
  json_str: str


@app.post("/json2html")
async def json2html(item: Item):
  _json = item.json_str
  prompt = "以下のJSONをHTMLに変換してください。:\n" + str(_json)
  html = get_completion(prompt)
  return html


class Item2(BaseModel):
  command: str
  html: str
  name: str


@app.post("/paint")
async def paint(item: Item2):
  command = item.command
  html = item.html
  prompt = f"""
  以下のhtmlに、以下の「操作」を加えたhtmlを出力してください。
  
  html: {html}
  操作: {command}
  """
  html = get_completion(prompt)
  return html


# @app.post("/upload_audio")
# async def upload_audio(file: Annotated[bytes, File()]):
#   audio_file = file.file
#   transcript = openai.Audio.transcribe("whisper-1", audio_file)
#   print(transcript)

#   return {"filename": file.filename}




@app.post("/oji")
async def paint(item: Item2):
  ojidata = ["ともえちゃん、可愛らしいネ😘（笑）😄可愛すぎてｵｼﾞｻﾝお仕事に集中できなくなっちゃいそうだよ😱(--;)^^;どうしてくれるンダ😃💗 ","ヤッホー😃(^_^)ゆあちゃん、元気かな⁉🤔❗❓（￣ー￣?）ゆあちゃんと今度イチャイチャ、したいなァ😄❗(^o^)土曜日、会社がお休みになったよ😚（笑）😘😍ゆあちゃんは都合どうかな🤔⁉カラオケ🎤ドウ(^o^)（笑）","こりんチャン、オッハー😄😃✋💕今日はもう寝ちゃったのかな（￣▽￣）✋(^^;;このホテル🏨、すごいキレイ🎵😍なんだって😄😘😃☀ ｵﾚと一緒に行こうヨ💗😃✋(^o^)😘なんちゃって💕(^з<) ","あいみちゃん、オッハー❗😄今日は楽しい時間をありがとうね😍💕すごく、楽しかっタヨ（笑）😚💗😄 ","ともみちゃんのお目々、キラキラ😃✋（笑）(^з<)😄してルネ😘💕💗こんなに可愛く(^o^)😄なっちゃったらお姫様みたいで小生困っちゃうヨ(TT)(--;)💦 ","マユカちゃん、オッハー😚マユカちゃんと今度イチャイチャ、したいナァ😚❗(^з<)😍よく頑張ったね💗😃☀ 😃♥ えらいえライ😚(^з<) ","晏希ﾁｬﾝ、髪の毛、切ったのかな❗❓似合いすぎだヨ(^o^)😄❗ｵｼﾞｻﾝ、本当に女優さんかと思っちゃったよ😃✋😍 ","砂知ちゃん、お早う😍今日も頑張ってネ😃☀ 💕😍 ","恋鈴チャン、そっちも台風🌀なのかな🤔❓❗❓月曜日は仕事〜✋❓😜⁉️このホテル🏩、すごいキレイ❗なんだって😃✋💕","ヤッホー😃✋(^3<)ひろえチャン、元気かな❓✋❓🤔⁉️今日はもう寝ちゃったのカナ😤くれぐれも体調に気をつケテ🙂( ´ ▽ ` )🛌","お疲れサマ😃♥こんな遅い時間💤✋😎に何をしているのかな!?😍突然だけど、りさちゃんは中華🍜好きカナ😜！?小生は明日から北京だよ😃😃✋テレビに映ちゃったらどうしよ〜(^o^)"]
  name = item.name
  command = item.command
  html = item.html
  
  prompt = f"""
  以下のhtmlに、以下の「操作」を加えたhtmlを出力してください。
  {ojidata}これはおじさん構文のデータファイルです。これを元に以下の条件を満たした以下の「翻訳前の文章」の文章を絵文字をたくさん含めたおじさん構文に翻訳してください。

＃条件
・文章内の名前は{name}
・敬語はあまり使わないこと(たまになら良い)
・名前には半角のカタカナで「ﾁｬﾝ」をつけること
・絵文字はいろいろな種類の絵文字を使うと好ましい
・絵文字をたくさん使うこと
・カタカナの半角をたまに用いること
・「可愛い」などの褒め言葉をよく使うこと
・極限まで「気持ち悪い」文章であること
・ただ絵文字などを付け加えるだけでなく翻訳前の文章におじさん構文ぽい言葉を付け加えること
・文章の意味が成りたっていること

＃翻訳前の文章{ command }
  """
  html += "<hr>" + "翻訳前の文章:" + "<br>" + command + "<br>" + "<br>" + "翻訳後の文章:" + "<br>" + get_completion(prompt)
  return html

@app.post("/upload_audio")
async def fileupload_post(request: Request):
  '''docstring
    アップロードされたファイルを保存する
    '''
  form = await request.form()
  for formdata in form:
    uploadfile = form[formdata]
    file_temp = uploadfile.file.read()
    # file = open("data/test.audio", mode="w")
    with open("data/test.mp3", "wb+") as f:
      f.write(file_temp)
    with open("data/test.mp3", "rb") as f:
      transcript_text = openai.Audio.transcribe("whisper-1", f)["text"]
    response = get_completion("この文章は「YOASOBI」という歌手の曲の歌詞です。この歌詞をもとにYOASOBIらしいの新しい歌詞を書いてください:" +  transcript_text)
  return {"transcript": transcript_text, "response": response}


if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
