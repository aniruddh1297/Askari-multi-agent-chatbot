import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";
import logo from './assets/logo2.png';

interface Message {
  role: "user" | "assistant";
  content: string;
}

const App: React.FC = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [agentMessage, setAgentMessage] = useState("");

  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null); // Auto-focus input

  const BACKEND_URL = "http://localhost:8000/chat";

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setStreamingContent("");
    setAgentMessage("");

    try {
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const reply = data.final_response || "⚠️ No response.";
      const route = data.route || "none";

      const routing =
        route === "hr"
          ? "Calling HR Agent..."
          : route === "it"
          ? "Calling IT Agent..."
          : route === "both"
          ? "HR & IT Agents assisting..."
          : "No specific agent matched. Trying best effort...";

      setAgentMessage(routing);
      await new Promise((r) => setTimeout(r, 1200));
      setAgentMessage("");

      let streamed = "";
      for (let i = 0; i < reply.length; i++) {
        streamed += reply[i];
        setStreamingContent(streamed);
        await new Promise((r) => setTimeout(r, 8));
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: streamed },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "❌ Error connecting to backend." },
      ]);
    } finally {
      setIsLoading(false);
      setStreamingContent("");
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    inputRef.current?.focus(); // Focus after every response
  }, [messages, streamingContent, agentMessage]);

  useEffect(() => {
    inputRef.current?.focus(); // Focus on initial render
  }, []);

  return (
    <div className="chat-container">
      <div className="header">
        <div className="logo-title">
          <img src={logo} alt="Askari Logo" className="logo" />
          <div className="title-block">
            <h1>ASKARI</h1>
            <p className="subheading">Intelligent Sentinel of Knowledge</p>
          </div>
        </div>
      </div>

      <div className="chat-box">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble ${msg.role === "user" ? "user" : "assistant"}`}
          >
            <ReactMarkdown
              components={{
                code: ({ node, inline, className, children, ...props }) =>
                  inline ? (
                    <code {...props} className={className}>
                      {children}
                    </code>
                  ) : (
                    <>{children}</> // ignore block code
                  ),
              }}
            >
              {msg.content}
            </ReactMarkdown>
          </div>
        ))}

        {isLoading && agentMessage && (
          <div className="chat-bubble assistant">
            <ReactMarkdown>{agentMessage}</ReactMarkdown>
          </div>
        )}

        {isLoading && (
          <div className="chat-bubble assistant">
            <ReactMarkdown>{streamingContent || "Thinking..."}</ReactMarkdown>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="input-row">
        <input
          ref={inputRef}
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !isLoading && handleSend()}
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
};

export default App;
