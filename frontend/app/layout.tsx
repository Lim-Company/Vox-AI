export const metadata = {
  title: "AI Secretary — Demo",
  description: "Live demo and lead capture"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "Inter, system-ui, Arial" }}>{children}</body>
    </html>
  );
}
