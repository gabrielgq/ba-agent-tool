"use client";

import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { FileText, History, BarChart2 } from "lucide-react";

// Placeholder Tab Components
const DocumentsList: React.FC = () => (
  <div className="p-4 text-center text-muted-foreground">
    Hier erscheinen Ihre hochgeladenen Dokumente.
  </div>
);
const HistoryList: React.FC = () => (
  <div className="p-4 text-center text-muted-foreground">
    Hier erscheint der Verlauf Ihrer Aktivitäten.
  </div>
);
const EmbeddingMonitor: React.FC = () => (
  <div className="p-4 text-center text-muted-foreground">
    Hier erscheint der Embedding Monitor.
  </div>
);

export function DocumentTabs() {
  const docCount = 0; // TODO: replace with actual state
  const embeddingCount = 0; // TODO: replace with actual state

  return (
    <Card>
      <Tabs defaultValue="documents" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger
            value="documents"
            className="flex items-center justify-center"
          >
            <FileText className="w-4 h-4 mr-2" />
            Dokumente
            <Badge variant="secondary" className="ml-2">
              {docCount}
            </Badge>
          </TabsTrigger>

          <TabsTrigger
            value="history"
            className="flex items-center justify-center"
          >
            <History className="w-4 h-4 mr-2" />
            Aktivitätsverlauf
          </TabsTrigger>

          <TabsTrigger
            value="embeddings"
            className="flex items-center justify-center"
          >
            <BarChart2 className="w-4 h-4 mr-2" />
            Embedding Monitor
            <Badge variant="secondary" className="ml-2">
              {embeddingCount}
            </Badge>
          </TabsTrigger>
        </TabsList>

        <CardContent className="p-0">
          <TabsContent value="documents">
            <DocumentsList />
          </TabsContent>
          <TabsContent value="history">
            <HistoryList />
          </TabsContent>
          <TabsContent value="embeddings">
            <EmbeddingMonitor />
          </TabsContent>
        </CardContent>
      </Tabs>
    </Card>
  );
}
