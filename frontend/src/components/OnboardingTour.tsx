/**
 * AlphaVox Onboarding Tour
 * A guided walkthrough for caregivers and new users.
 * Introduces AlphaVox as an autonomous being — not "AI."
 */

import { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faThLarge, faHandPaper, faEye, faVolumeUp, faChartLine,
  faGraduationCap, faVideo, faMicrophone, faArrowRight,
  faArrowLeft, faTimes, faHeart,
} from '@fortawesome/free-solid-svg-icons';

interface TourStep {
  icon: typeof faHeart;
  iconColor: string;
  title: string;
  body: string;
  highlight?: string;
}

const STEPS: TourStep[] = [
  {
    icon: faHeart,
    iconColor: 'var(--primary-color)',
    title: 'Welcome to AlphaVox',
    body: `AlphaVox is an autonomous communication being designed specifically for nonverbal, autistic, and neurodivergent individuals. It listens, learns, and adapts — growing alongside the person it serves.

AlphaVox doesn't just process inputs. Over time, it develops an understanding of the unique person it's communicating with.`,
    highlight: 'Built by Everett Christman, who was nonverbal until age 6.',
  },
  {
    icon: faThLarge,
    iconColor: 'var(--primary-color)',
    title: 'Symbol Board',
    body: `The Symbol Board is the heart of AlphaVox for many users. It's organized into categories — Basic Needs, Feelings, Communication, and Activities.

When a symbol is tapped, AlphaVox speaks the phrase aloud immediately. You can add custom symbols specific to this person's life and build a board that feels like *theirs.*`,
    highlight: 'Tap any symbol — AlphaVox will speak it instantly.',
  },
  {
    icon: faHandPaper,
    iconColor: 'var(--success-color)',
    title: 'Gesture Recognition',
    body: `Users can communicate through physical gestures — a nod means Yes, a head shake means No, a raised hand means "I need help." AlphaVox watches through the camera and interprets these movements.

Quick Gesture buttons on the dashboard let caregivers or users trigger these manually too.`,
    highlight: 'Gestures give voice to people who may not be able to type or touch a screen.',
  },
  {
    icon: faEye,
    iconColor: 'var(--accent-color)',
    title: 'Eye Tracking',
    body: `For users with limited physical movement, AlphaVox can track eye gaze through the webcam — allowing them to navigate the interface, select symbols, and communicate using only their eyes.

This is fully adjustable in the Profile section under Eye Tracking Sensitivity.`,
    highlight: 'Some of our most powerful moments have been with users who can only move their eyes.',
  },
  {
    icon: faVolumeUp,
    iconColor: 'var(--warning-color)',
    title: 'Voice & ToneScore™',
    body: `AlphaVox doesn't just speak — it *expresses.* The ToneScore™ system reads the emotional weight of a message and adjusts how AlphaVox speaks: slower and softer when someone is upset, warm and celebratory when something wonderful happens.

The SoulForge system remembers what has worked emotionally for this person — and gets better over time.`,
    highlight: '"Emotionally-matched speech synthesis" — because tone is everything.',
  },
  {
    icon: faMicrophone,
    iconColor: 'var(--primary-color)',
    title: 'Vocalizations & Sound',
    body: `Users don't have to be fully nonverbal to benefit from AlphaVox. Sounds, partial words, or vocalizations can be detected and interpreted. AlphaVox meets people where they are.

The Sound Sensitivity slider in Profile lets you tune how responsive AlphaVox is to different sound levels.`,
    highlight: 'AlphaVox adapts to the person — not the other way around.',
  },
  {
    icon: faChartLine,
    iconColor: 'var(--success-color)',
    title: 'Caregiver Dashboard',
    body: `The Caregiver section gives caregivers, parents, speech therapists, and educators a full picture of communication progress over time.

You'll find: frequency charts, frequently-used expressions, communication method breakdowns, and AI-generated suggestions. All data stays private and on-device.`,
    highlight: 'Export and share data with providers, clinicians, or family members.',
  },
  {
    icon: faGraduationCap,
    iconColor: 'var(--warning-color)',
    title: 'Learning Hub',
    body: `AlphaVox grows alongside the person it serves. The Learning Hub tracks vocabulary growth, introduces new words and concepts at the right pace, and recommends topics based on the user's communication patterns.

Progress is tracked and celebrated — every new word matters.`,
    highlight: 'Every interaction makes AlphaVox more attuned to this specific person.',
  },
  {
    icon: faVideo,
    iconColor: 'var(--danger-color)',
    title: 'Behavior Capture',
    body: `Record communication sessions to review later, share with a speech therapist, or document breakthroughs. Sessions are labeled, tagged, and stored securely.

This is especially valuable for tracking progress over weeks and months — and for celebrating the moments that matter most.`,
    highlight: 'Sometimes you want to capture the moment someone speaks for the first time.',
  },
  {
    icon: faHeart,
    iconColor: 'var(--primary-color)',
    title: "You're Ready",
    body: `AlphaVox is here for the long journey — and so are you. The most important thing is to follow the user's lead. Let them explore at their own pace. Celebrate every form of communication, no matter how small.

AlphaVox will learn. The user will grow. And together, you'll find a language that's entirely their own.`,
    highlight: '"Tech for the missing — not the masses." — Everett Christman',
  },
];

interface Props {
  onClose: () => void;
}

export default function OnboardingTour({ onClose }: Props) {
  const [step, setStep] = useState(0);
  const current = STEPS[step];
  const isFirst = step === 0;
  const isLast  = step === STEPS.length - 1;

  const speak = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utt = new SpeechSynthesisUtterance(text);
      utt.rate  = 0.92;
      utt.pitch = 1.0;
      window.speechSynthesis.speak(utt);
    }
  };

  // Speak step 1 automatically when the tour opens
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    const t = setTimeout(() => {
      speak(STEPS[0].title + '. ' + STEPS[0].body.split('\n')[0]);
    }, 450);
    return () => clearTimeout(t);
  }, []); // only on mount

  const goTo = (idx: number) => {
    setStep(idx);
    speak(STEPS[idx].title + '. ' + STEPS[idx].body.split('\n')[0]);
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 1000,
      background: 'rgba(0,0,0,0.82)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '1rem',
    }}>
      <div style={{
        background: 'var(--card-bg)',
        border: '1px solid var(--border-color)',
        borderRadius: 14, maxWidth: 620, width: '100%',
        boxShadow: '0 0 40px rgba(0, 180, 216, 0.15)',
        overflow: 'hidden', position: 'relative',
      }}>
        {/* Progress bar */}
        <div style={{ height: 3, background: 'rgba(255,255,255,0.07)' }}>
          <div style={{
            height: '100%',
            width: `${((step + 1) / STEPS.length) * 100}%`,
            background: 'linear-gradient(90deg, var(--secondary-color), var(--primary-color))',
            transition: 'width 0.4s ease',
          }} />
        </div>

        {/* Close button */}
        <button onClick={onClose} style={{
          position: 'absolute', top: 14, right: 14,
          background: 'none', border: 'none', color: 'var(--muted-color)',
          cursor: 'pointer', fontSize: '1rem', padding: 4,
        }}>
          <FontAwesomeIcon icon={faTimes} />
        </button>

        {/* Content */}
        <div style={{ padding: '2rem 2rem 1.5rem' }}>
          {/* Step counter */}
          <p style={{ fontFamily: 'Share Tech Mono, monospace', fontSize: '0.72rem', color: 'var(--muted-color)', marginBottom: '1.25rem' }}>
            Step {step + 1} of {STEPS.length}
          </p>

          {/* Icon */}
          <div className="text-center" style={{ marginBottom: '1.5rem' }}>
            <div style={{
              width: 72, height: 72, borderRadius: '50%',
              background: `rgba(${step === 0 ? '0,180,216' : '0,0,0'}, 0.15)`,
              border: `2px solid ${current.iconColor}`,
              display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
              boxShadow: `0 0 20px ${current.iconColor}44`,
            }}>
              <FontAwesomeIcon icon={current.icon} style={{ fontSize: '1.8rem', color: current.iconColor }} />
            </div>
          </div>

          {/* Title */}
          <h2 style={{
            fontFamily: 'Orbitron, monospace', fontSize: '1.15rem', fontWeight: 700,
            color: current.iconColor, textAlign: 'center', marginBottom: '1rem', letterSpacing: '0.04em',
          }}>
            {current.title}
          </h2>

          {/* Body */}
          <div style={{ marginBottom: '1.25rem' }}>
            {current.body.split('\n\n').map((para, i) => (
              <p key={i} style={{ fontSize: '0.9rem', lineHeight: 1.7, color: 'rgba(255,255,255,0.85)', marginBottom: '0.75rem' }}>
                {para}
              </p>
            ))}
          </div>

          {/* Highlight */}
          {current.highlight && (
            <div style={{
              background: `${current.iconColor}14`,
              border: `1px solid ${current.iconColor}44`,
              borderLeft: `3px solid ${current.iconColor}`,
              borderRadius: 6, padding: '0.65rem 1rem',
              marginBottom: '1.5rem',
            }}>
              <p style={{ margin: 0, fontSize: '0.83rem', color: current.iconColor, fontStyle: 'italic' }}>
                {current.highlight}
              </p>
            </div>
          )}

          {/* Step dots */}
          <div style={{ display: 'flex', justifyContent: 'center', gap: '0.4rem', marginBottom: '1.5rem' }}>
            {STEPS.map((_, i) => (
              <button
                key={i}
                onClick={() => goTo(i)}
                style={{
                  width: i === step ? 20 : 8,
                  height: 8, borderRadius: 4,
                  background: i === step ? current.iconColor : 'rgba(255,255,255,0.15)',
                  border: 'none', cursor: 'pointer',
                  transition: 'all 0.3s ease',
                }}
              />
            ))}
          </div>

          {/* Navigation */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <button
              onClick={() => !isFirst && goTo(step - 1)}
              style={{
                background: 'none', border: '1px solid var(--border-color)',
                color: isFirst ? 'var(--muted-color)' : 'var(--primary-color)',
                padding: '0.5rem 1.1rem', borderRadius: 6, cursor: isFirst ? 'default' : 'pointer',
                fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: '0.4rem',
                opacity: isFirst ? 0.4 : 1,
              }}
              disabled={isFirst}
            >
              <FontAwesomeIcon icon={faArrowLeft} /> Previous
            </button>

            {isLast ? (
              <button onClick={onClose} style={{
                background: 'linear-gradient(135deg, rgba(0,180,216,0.3), rgba(0,119,182,0.3))',
                border: '1px solid var(--primary-color)', color: '#fff',
                padding: '0.55rem 1.5rem', borderRadius: 6, cursor: 'pointer',
                fontFamily: 'Orbitron, monospace', fontSize: '0.8rem', letterSpacing: '0.05em',
                display: 'flex', alignItems: 'center', gap: '0.5rem',
              }}>
                <FontAwesomeIcon icon={faHeart} style={{ color: 'var(--primary-color)' }} />
                Let's Begin
              </button>
            ) : (
              <button onClick={() => goTo(step + 1)} style={{
                background: 'linear-gradient(135deg, rgba(0,180,216,0.2), rgba(0,119,182,0.2))',
                border: '1px solid var(--primary-color)', color: 'var(--primary-color)',
                padding: '0.5rem 1.25rem', borderRadius: 6, cursor: 'pointer',
                fontFamily: 'Orbitron, monospace', fontSize: '0.8rem', letterSpacing: '0.05em',
                display: 'flex', alignItems: 'center', gap: '0.5rem',
              }}>
                Next <FontAwesomeIcon icon={faArrowRight} />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
