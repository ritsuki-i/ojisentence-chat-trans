const inputField = document.getElementById("input-field");
const chatArea = document.getElementById("chat-area");
const sendButton = document.getElementById("send-button");
const resultArea = document.getElementById("result-area"); // 追加

function isResult(response) {
    return response.startsWith("あなたはおじさんです。");
}

async function getFirstResponse() {
    const response = await fetch("/");
    console.log("Initial response:", response);
    const result = await response.json();
    chatArea.innerHTML += "Chatbot: " + result.response + "<br>";
}

getFirstResponse();

sendButton.onclick = async () => {
    document.getElementById("send-button").innerHTML = "　送信中"
    const user_input = inputField.value;
    const data = { "user_input": user_input };
    console.log(data);
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    console.log("Chat response:", response);
    const result = await response.json();

    chatArea.innerHTML += "You: " + user_input + "<br>";
    
    if (isResult(result.response)) {
        resultArea.innerHTML = "診断結果: " + result.response; // 結果を resultArea に表示
    } else {
        chatArea.innerHTML += "<br>"+"Chatbot: " + result.response + "<br>";
    }
    inputField.value = "";
    document.getElementById("send-button").innerHTML = "　送信する"
};