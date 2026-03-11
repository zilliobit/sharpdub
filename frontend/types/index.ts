/* export interface ExceptionWord {
  id: string
  word: string
  createdAt: Date
}

export interface SpellingRule {
  id: string
  original: string
  replacement: string
  createdAt: Date
}

export interface Glossary {
  id: string
  name: string
  description: string
  sourceLanguage: string
  targetLanguage: string
  terms: GlossaryTerm[]
  createdAt: Date
  updatedAt: Date
}

export interface GlossaryTerm {
  id: string
  source: string
  target: string
}

export interface TimelineSegment {
  id: string
  start: number
  end: number
  text: string
  translatedText: string
}

export interface MediaFile {
  id: string
  name: string
  type: 'video' | 'audio' | 'document'
  size: number
  uploadedAt: Date
  duration?: number
  thumbnail?: string
}

export interface Project {
  id: string
  name: string
  description: string
  sourceLanguage: string
  targetLanguage: string
  mediaFile?: MediaFile
  segments: TimelineSegment[]
  exceptions: string[]
  glossaryId?: string
  createdAt: Date
  updatedAt: Date
  status: 'draft' | 'processing' | 'completed'
}
 */

export type APIResponse = {
  success: boolean;
  message?: string;
};
