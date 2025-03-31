"use client"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

// Sample data - in a real app this would come from your backend
const traitScores = {
  analytical: 4.5,
  creative: 3.2,
  "detail-oriented": 4.8,
  patient: 2.5,
  communicative: 3.7,
}

const careerRecommendations = [
  {
    occupation: "Software Developer",
    description: "Develops applications and systems using programming languages",
    education_required: "Bachelor's degree in Computer Science",
    score: 0.92,
  },
  {
    occupation: "Data Scientist",
    description: "Analyzes data and builds models to extract insights",
    education_required: "Master's degree in Data Science or related field",
    score: 0.87,
  },
  {
    occupation: "UX Designer",
    description: "Designs user interfaces and experiences for digital products",
    education_required: "Bachelor's degree in Design or related field",
    score: 0.78,
  },
]

const universityRecommendations = [
  {
    university: "MIT",
    location: "Massachusetts",
    programs: "Computer Science, Engineering, Mathematics",
    cost: 55000,
    acceptance_rate: 0.07,
    graduation_rate: 0.94,
    score: 0.89,
  },
  {
    university: "Stanford",
    location: "California",
    programs: "Computer Science, Business, Medicine",
    cost: 57000,
    acceptance_rate: 0.05,
    graduation_rate: 0.96,
    score: 0.85,
  },
  {
    university: "Georgia Tech",
    location: "Georgia",
    programs: "Engineering, Computer Science, Mathematics",
    cost: 33000,
    acceptance_rate: 0.21,
    graduation_rate: 0.87,
    score: 0.82,
  },
]

export default function Results() {
  return (
    <div className="container mx-auto px-4 py-8">
      <header className="text-center my-8">
        <h1 className="text-3xl font-bold mb-2">Your Results</h1>
        <p className="text-muted-foreground">Based on your personality and interests, here are our recommendations</p>
      </header>

      <div className="max-w-4xl mx-auto space-y-8">
        {/* Personality Profile */}
        <Card className="shadow">
          <CardHeader className="bg-primary text-primary-foreground">
            <h2 className="text-xl font-semibold">Your Personality Profile</h2>
          </CardHeader>
          <CardContent className="p-6">
            <div className="space-y-4">
              {Object.entries(traitScores).map(([trait, score]) => (
                <div key={trait} className="flex items-center justify-between">
                  <span className="font-medium capitalize w-1/3">{trait}</span>
                  <div className="w-2/3 flex items-center gap-4">
                    <Progress value={(score / 5) * 100} className="h-2 flex-1" />
                    <span className="text-sm font-medium w-10">{score.toFixed(1)}/5</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Career Recommendations */}
        <Card className="shadow">
          <CardHeader className="bg-green-600 text-white">
            <h2 className="text-xl font-semibold">Recommended Careers</h2>
          </CardHeader>
          <CardContent className="p-6">
            <div className="space-y-6">
              {careerRecommendations.map((career, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-medium">{career.occupation}</h3>
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                      {Math.round(career.score * 100)}% Match
                    </Badge>
                  </div>
                  <p className="text-muted-foreground">{career.description}</p>
                  <p className="text-sm">
                    <strong>Education Required:</strong> {career.education_required}
                  </p>
                  {index < careerRecommendations.length - 1 && <hr className="my-4" />}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* University Recommendations */}
        <Card className="shadow">
          <CardHeader className="bg-blue-600 text-white">
            <h2 className="text-xl font-semibold">Recommended Universities</h2>
          </CardHeader>
          <CardContent className="p-6">
            <div className="space-y-6">
              {universityRecommendations.map((university, index) => (
                <div key={index} className="space-y-3">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-medium">{university.university}</h3>
                    <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                      {Math.round(university.score * 100)}% Match
                    </Badge>
                  </div>
                  <p>
                    <strong>Location:</strong> {university.location}
                  </p>
                  <p>
                    <strong>Programs:</strong> {university.programs}
                  </p>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <p>
                        <strong>Annual Cost:</strong>
                      </p>
                      <p>${university.cost.toLocaleString()}</p>
                    </div>
                    <div>
                      <p>
                        <strong>Acceptance Rate:</strong>
                      </p>
                      <p>{(university.acceptance_rate * 100).toFixed(1)}%</p>
                    </div>
                    <div>
                      <p>
                        <strong>Graduation Rate:</strong>
                      </p>
                      <p>{(university.graduation_rate * 100).toFixed(1)}%</p>
                    </div>
                  </div>
                  {index < universityRecommendations.length - 1 && <hr className="my-4" />}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Study Plan Generator */}
        <Card className="shadow">
          <CardHeader className="bg-amber-500 text-white">
            <h2 className="text-xl font-semibold">Generate Study Plan</h2>
          </CardHeader>
          <CardContent className="p-6 text-center">
            <p className="mb-4">Want to see a detailed study plan for your chosen major?</p>
            <Link href="/study-plan">
              <Button variant="default" size="lg" className="bg-amber-500 hover:bg-amber-600">
                Create Study Plan
              </Button>
            </Link>
          </CardContent>
        </Card>

        <div className="text-center mt-8">
          <Link href="/">
            <Button variant="outline">Start Over</Button>
          </Link>
        </div>
      </div>

      <footer className="text-center py-6 mt-12 text-sm text-muted-foreground">
        <p>© 2023 Career Advisor AI | Developed for AI Hackathon</p>
      </footer>
    </div>
  )
}

