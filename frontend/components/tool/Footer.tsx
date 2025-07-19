export function Footer() {
  return (
    <footer className="w-full bg-secondary text-secondary-foreground mt-8">
      <div className="container mx-auto py-6 text-center">
        <p className="text-sm opacity-90">
          © {new Date().getFullYear()} Business Analyst Agent. Powered by Gemini
          AI.
        </p>
      </div>
    </footer>
  );
}
