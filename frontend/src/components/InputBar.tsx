import { useState } from 'react'
import { processInput, synthesizeTTS } from '../services/api'

interface Props {
  userId: string
}

interface Message {
  role: 'user' | 'alpha'
  text: string
}

export default function InputBar({ userId }: Props) {
  const [text, setText] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  const send = async () => {
    const trimmed = text.trim()
    if (!trimmed || loading) return

    setMessages((m) => [...m, { role: 'user', text: trimmed }])
    setText('')
    setLoading(true)

    try {
      const result = await processInput({ text: trimmed, user_id: userId })
      const reply = result.message ?? 'Processing…'
      setMessages((m) => [...m, { role: 'alpha', text: reply }])
      // Speak the response
      await synthesizeTTS({ text: reply })
    } catch {
      setMessages((m) => [...m, { role: 'alpha', text: '(Connection error – check backend)' }])
    } finally {
      setLoading(false)
    }
  }

  const onKey = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <div style={styles.wrapper}>
      <div style={styles.feed}>
        {messages.map((m, i) => (
          <div key={i} style={{ ...styles.bubble, ...(m.role === 'user' ? styles.userBubble : styles.alphaBubble) }}>
            {m.text}
          </div>
        ))}
        {loading && <div style={{ ...styles.bubble, ...styles.alphaBubble }}>...</div>}
      </div>

      <div style={styles.bar}>
        <textarea
          style={styles.textarea}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={onKey}
          placeholder="Type or speak…"
          rows={2}
        />
        <button style={styles.send} onClick={send} disabled={loading || !text.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  wrapper: { width: '100%', maxWidth: '720px', display: 'flex', flexDirection: 'column', gap: '1rem' },
  feed: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
    minHeight: '200px',
    maxHeight: '480px',
    overflowY: 'auto',
    background: 'var(--color-surface)',
    borderRadius: '0.75rem',
    padding: '1.25rem',
  },
  bubble: {
    padding: '0.6rem 1rem',
    borderRadius: '0.6rem',
    maxWidth: '80%',
    lineHeight: 1.5,
    fontSize: '0.95rem',
  },
  userBubble: { alignSelf: 'flex-end', background: 'var(--color-primary)', color: '#fff' },
  alphaBubble: { alignSelf: 'flex-start', background: '#1e1e2e', color: 'var(--color-text)' },
  bar: { display: 'flex', gap: '0.75rem', alignItems: 'flex-end' },
  textarea: {
    flex: 1,
    padding: '0.75rem 1rem',
    fontSize: '0.95rem',
    borderRadius: '0.5rem',
    border: '1px solid #2a2a3a',
    background: 'var(--color-surface)',
    color: 'var(--color-text)',
    resize: 'none',
    outline: 'none',
  },
  send: {
    padding: '0.75rem 1.5rem',
    borderRadius: '0.5rem',
    border: 'none',
    background: 'var(--color-primary)',
    color: '#fff',
    fontWeight: 600,
    cursor: 'pointer',
    fontSize: '0.95rem',
  },
}
