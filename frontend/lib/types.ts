export interface DocumentFile {
  id: string;
  name: string;
  type: string;
  size: number;
  content: string;
  uploadDate: Date;
  embeddings: number;
  processed: boolean;
}

export interface HistoryItem {
  id: number;
  action: string;
  type: 'upload' | 'chat' | 'delete' | 'download';
  details?: Record<string, any>;
  timestamp: Date;
}

export interface Template {
  id: string;
  name: string;
  content: string;
}

export interface ChatMessage {
  sender: 'user' | 'assistant';
  content: string;
}