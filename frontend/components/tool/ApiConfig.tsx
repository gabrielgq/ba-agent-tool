"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Box } from "lucide-react";

export function ApiConfig() {
  const [apiKey, setApiKey] = useState("");
  const [status, setStatus] = useState<
    "connected" | "disconnected" | "connecting"
  >("disconnected");

  const handleConnect = () => {
    if (!apiKey) {
      // Add toast notification later
      console.error("API Key is required");
      return;
    }
    setStatus("connecting");
    // Simulate API connection
    setTimeout(() => {
      setStatus("connected");
      // Add toast notification
    }, 1500);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <Box className="w-5 h-5 text-primary" />
          Gemini AI Konfiguration
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input
            type="password"
            placeholder="Geben Sie Ihren Gemini API-Schlüssel ein..."
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
          <div className="flex gap-2">
            <Button onClick={handleConnect} disabled={status === "connecting"}>
              {status === "connecting" ? "Verbinde..." : "Verbinden"}
            </Button>
            <Button variant="secondary" disabled={status !== "connected"}>
              Test Verbindung
            </Button>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                status === "connected"
                  ? "bg-green-500"
                  : status === "connecting"
                  ? "bg-yellow-500 animate-pulse"
                  : "bg-red-500"
              }`}
            ></span>
            <span className="text-muted-foreground">
              {status === "connected" ? "Verbunden" : "Nicht verbunden"}
            </span>
          </div>
          <p className="text-xs text-muted-foreground">
            Benötigen Sie einen API-Schlüssel? Besuchen Sie{" "}
            <a
              href="https://makersuite.google.com/app/apikey"
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              Google AI Studio
            </a>{" "}
            um einen kostenlosen Schlüssel zu erhalten.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
