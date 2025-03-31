"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"

// Sample personality questions
const personalityQuestions = [
  {
    id: "analytical",
    question: "Do you enjoy solving complex problems and puzzles?",
    trait: "analytical",
  },
  {
    id: "creative",
    question: "Do you often come up with unique ideas or solutions?",
    trait: "creative",
  },
  {
    id: "detail_oriented",
    question: "Do you pay close attention to details and notice small errors?",
    trait: "detail-oriented",
  },
  {
    id: "patient",
    question: "Are you patient when dealing with challenging situations?",
    trait: "patient",
  },
  {
    id: "communicative",
    question: "Do you enjoy explaining concepts to others?",
    trait: "communicative",
  },
]

export default function PersonalityAssessment() {
  const router = useRouter()
  const [answers, setAnswers] = useState<Record<string, number>>({})

  const handleChange = (questionId: string, value: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: Number.parseInt(value),
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would save this to state/context/session
    console.log("Personality answers:", answers)
    router.push("/assessment/interests")
  }

  const isComplete = personalityQuestions.every((q) => answers[q.id])

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="text-center my-8">
        <h1 className="text-3xl font-bold mb-2">Personality Assessment</h1>
        <p className="text-muted-foreground mb-4">Step 1 of 2: Tell us about your personality traits</p>
        <Progress value={50} className="w-full max-w-md mx-auto h-2" />
      </header>

      <div className="flex justify-center">
        <Card className="w-full max-w-2xl shadow">
          <CardContent className="p-6">
            <form onSubmit={handleSubmit}>
              <div className="space-y-8">
                {personalityQuestions.map((question) => (
                  <div key={question.id} className="p-4 bg-muted/50 rounded-lg">
                    <h3 className="font-medium mb-4">{question.question}</h3>
                    <div>
                      <div className="flex justify-between mb-2 text-sm text-muted-foreground">
                        <span>Not at all</span>
                        <span>Very much</span>
                      </div>
                      <RadioGroup
                        value={answers[question.id]?.toString()}
                        onValueChange={(value) => handleChange(question.id, value)}
                        className="flex justify-between"
                      >
                        {[1, 2, 3, 4, 5].map((value) => (
                          <div key={value} className="flex flex-col items-center">
                            <RadioGroupItem value={value.toString()} id={`${question.id}-${value}`} className="mb-1" />
                            <Label htmlFor={`${question.id}-${value}`}>{value}</Label>
                          </div>
                        ))}
                      </RadioGroup>
                    </div>
                  </div>
                ))}
              </div>

              <div className="text-center mt-8">
                <Button type="submit" size="lg" disabled={!isComplete}>
                  Continue to Interests
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      <footer className="text-center py-6 mt-12 text-sm text-muted-foreground">
        <p>© 2023 Career Advisor AI | Developed for AI Hackathon</p>
      </footer>
    </div>
  )
}

