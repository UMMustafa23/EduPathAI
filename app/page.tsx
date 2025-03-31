import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="text-center my-12">
        <h1 className="text-4xl font-bold tracking-tight mb-4">Career Advisor AI</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Find your perfect university and career path with AI-powered recommendations
        </p>
      </header>

      <div className="flex justify-center">
        <Card className="w-full max-w-3xl shadow-lg">
          <CardContent className="p-8">
            <h2 className="text-2xl font-semibold text-center mb-8">How It Works</h2>

            <div className="space-y-8">
              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xl font-bold">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-medium mb-2">Personality Assessment</h3>
                  <p className="text-muted-foreground">
                    Answer questions about your personality traits to help us understand your working style and
                    preferences.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xl font-bold">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-medium mb-2">Interest Assessment</h3>
                  <p className="text-muted-foreground">
                    Tell us about your interests and subject preferences to identify potential career paths.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xl font-bold">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-medium mb-2">Get Recommendations</h3>
                  <p className="text-muted-foreground">
                    Receive personalized career and university recommendations based on your profile.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-6">
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xl font-bold">
                  4
                </div>
                <div>
                  <h3 className="text-xl font-medium mb-2">Study Plan</h3>
                  <p className="text-muted-foreground">
                    Generate a detailed study plan for your chosen major with resources and timeline.
                  </p>
                </div>
              </div>
            </div>

            <div className="text-center mt-10">
              <Link href="/assessment/personality">
                <Button size="lg" className="px-8">
                  Start Assessment
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      <footer className="text-center py-6 mt-12 text-sm text-muted-foreground">
        <p>© 2023 Career Advisor AI | Developed for AI Hackathon</p>
      </footer>
    </div>
  )
}

