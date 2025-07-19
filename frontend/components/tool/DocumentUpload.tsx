"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { UploadCloud, Loader2 } from "lucide-react";

export function DocumentUpload() {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles]);
    // Simulate processing
    setIsProcessing(true);
    setProgress(0);
    const timer = setInterval(() => {
      setProgress((oldProgress) => {
        if (oldProgress === 100) {
          clearInterval(timer);
          setIsProcessing(false);
          return 100;
        }
        const diff = Math.random() * 10;
        return Math.min(oldProgress + diff, 100);
      });
    }, 500);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "text/plain": [".txt"],
      "application/pdf": [".pdf"],
      "text/markdown": [".md"],
      "text/csv": [".csv"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        [".docx"],
      "application/json": [".json"],
    },
  });

  return (
    <Card>
      <CardContent className="p-6">
        <div
          {...getRootProps()}
          className={`flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg cursor-pointer transition-colors ${
            isDragActive
              ? "border-primary bg-accent"
              : "border-border hover:border-primary/50"
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex items-center justify-center w-12 h-12 bg-primary text-primary-foreground rounded-lg mb-4">
            <UploadCloud className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold mb-1">Dokumente hochladen</h3>
          <p className="text-muted-foreground mb-4 text-sm">
            Ziehen Sie Dateien hierher oder klicken Sie, um sie auszuwählen
          </p>
          <Button type="button" variant="secondary">
            Dateien auswählen
          </Button>
        </div>

        {isProcessing && (
          <div className="mt-4 text-center">
            <div className="flex items-center justify-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Dokumente werden verarbeitet...</span>
            </div>
            <Progress value={progress} className="w-full mt-2 h-2" />
            <p className="text-xs text-muted-foreground mt-1">
              {Math.round(progress)}%
            </p>
          </div>
        )}

        {files.length > 0 && !isProcessing && (
          <div className="mt-4">
            <h4 className="font-semibold">Hochgeladene Dateien:</h4>
            <ul className="list-disc list-inside text-sm text-muted-foreground">
              {files.map((file, i) => (
                <li key={i}>{file.name}</li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
