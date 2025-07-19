"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Bot, Send, User, FileSignature } from "lucide-react";
import { type ChatMessage } from "@/lib/types";

export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      sender: "assistant",
      content:
        "Willkommen! Verbinden Sie sich mit Gemini AI, laden Sie Ihre Dokumente hoch und stellen Sie Ihre Fragen.",
    },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;
    const userMessage: ChatMessage = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    // Simulate AI response
    setTimeout(() => {
      const assistantMessage: ChatMessage = {
        sender: "assistant",
        content: "Dies ist eine simulierte Antwort auf Ihre Frage.",
      };
      setMessages((prev) => [...prev, assistantMessage]);
    }, 1000);
  };

  return (
    <Card className="flex flex-col h-[70vh]">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Bot className="text-primary" />
            KI-Assistent für Dokumentenanalyse
          </CardTitle>
          <Button variant="outline" size="sm">
            <FileSignature className="w-4 h-4 mr-2" />
            Vorlagen
          </Button>
        </div>
      </CardHeader>
      <CardContent className="flex-1 p-0">
        <ScrollArea className="h-full p-4">
          <div className="space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex items-start gap-3 ${
                  msg.sender === "user" ? "justify-end" : ""
                }`}
              >
                {msg.sender === "assistant" && (
                  <div className="p-2 rounded-full bg-muted">
                    <Bot className="w-5 h-5 text-primary" />
                  </div>
                )}
                <div
                  className={`rounded-lg p-3 max-w-[80%] ${
                    msg.sender === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted"
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                </div>
                {msg.sender === "user" && (
                  <div className="p-2 rounded-full bg-muted">
                    <User className="w-5 h-5" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
      <CardFooter className="p-4 border-t">
        <div className="flex w-full items-center space-x-2">
          <Textarea
            placeholder="Stellen Sie eine Frage zu Ihren Dokumenten..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            rows={1}
            className="min-h-[40px] resize-none"
          />
          <Button onClick={handleSend}>
            Senden <Send className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </CardFooter>
    </Card>
  );
}
