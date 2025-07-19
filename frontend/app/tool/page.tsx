import { Header } from "@/components/tool/Header";
import { Footer } from "@/components/tool/Footer";
import { ApiConfig } from "@/components/tool/ApiConfig";
import { DocumentUpload } from "@/components/tool/DocumentUpload";
import { DocumentTabs } from "@/components/tool/DocumentTabs";
import { ChatInterface } from "@/components/tool/ChatInterface";

export default function ToolPage() {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header />
      <main className="flex-1 container mx-auto py-8 px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-1 space-y-6">
            <ApiConfig />
            <DocumentUpload />
            <DocumentTabs />
          </div>

          {/* Right Column */}
          <div className="md:col-span-1 lg:col-span-2">
            <ChatInterface />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
