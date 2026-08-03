import { useEffect, useRef, useState } from "react"
import { AnimatePresence, motion } from "framer-motion"
import type { Frame } from "@/data/project-frames"

/* Real 10x Visuals project photography, adapted from the pasted
   reference (which used Unsplash stock and a hover-grow row). Redone
   per Hunter's feedback: black and white, edge-to-edge horizontal
   scroll starting flush at the left of the viewport (no void before
   the first frame) at every breakpoint — not just mobile — and click
   to open full screen. The click-to-expand/Escape/focus-return pattern
   mirrors carousel-3d.tsx exactly, same as its own keyboard fixes. */
export default function ProjectGallery({ frames }: { frames: Frame[] }) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
  const activeFrame = activeIndex !== null ? frames[activeIndex] : null
  const returnFocusRef = useRef<HTMLElement | null>(null)
  const closeBtnRef = useRef<HTMLButtonElement | null>(null)

  const handleOpen = (index: number, el: HTMLElement) => {
    returnFocusRef.current = el
    setActiveIndex(index)
  }

  const handleClose = () => {
    setActiveIndex(null)
    returnFocusRef.current?.focus()
  }

  useEffect(() => {
    if (activeIndex === null) return
    closeBtnRef.current?.focus()
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") { e.preventDefault(); handleClose() }
    }
    document.addEventListener("keydown", onKeyDown)
    return () => document.removeEventListener("keydown", onKeyDown)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIndex])

  return (
    <div className="tdx:relative">
      <div
        className="tdx:flex tdx:gap-3 tdx:h-64 tdx:sm:h-[480px] tdx:overflow-x-auto"
        style={{ width: "100vw", marginLeft: "calc(50% - 50vw)" }}
      >
        {frames.map((frame, idx) => (
          <div
            key={idx}
            role="button"
            tabIndex={0}
            aria-label={`Expand: ${frame.alt}`}
            onClick={(e) => handleOpen(idx, e.currentTarget)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault()
                handleOpen(idx, e.currentTarget)
              }
            }}
            className="tdx:group tdx:relative tdx:flex-none tdx:w-64 tdx:sm:w-96 tdx:h-full tdx:overflow-hidden tdx:cursor-pointer tdx:outline-none tdx:focus-visible:ring-2 tdx:focus-visible:ring-white/70"
          >
            <img
              className="tdx:h-full tdx:w-full tdx:object-cover tdx:object-center tdx:grayscale"
              src={frame.src}
              alt={frame.alt}
            />
            <div className="tdx:absolute tdx:inset-0 tdx:flex tdx:items-center tdx:justify-center tdx:bg-black/0 tdx:group-hover:bg-black/30 tdx:transition-colors tdx:duration-300">
              <span className="tdx:flex tdx:items-center tdx:justify-center tdx:w-11 tdx:h-11 tdx:rounded-full tdx:bg-white/95 tdx:opacity-0 tdx:scale-75 tdx:group-hover:opacity-100 tdx:group-hover:scale-100 tdx:group-focus-visible:opacity-100 tdx:group-focus-visible:scale-100 tdx:transition-all tdx:duration-300">
                <svg viewBox="0 0 24 24" fill="none" className="tdx:w-4 tdx:h-4" aria-hidden="true">
                  <path d="M4 10V4h6M20 14v6h-6M4 4l7 7M20 20l-7-7" stroke="#111519" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
            </div>
          </div>
        ))}
        {/* Trailing spacer so the last frame doesn't sit flush against
            the right edge with nothing to signal the row has ended. */}
        <div className="tdx:flex-none tdx:w-4" aria-hidden="true" />
      </div>

      <AnimatePresence>
        {activeFrame && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
            role="dialog"
            aria-modal="true"
            aria-label={activeFrame.alt}
            className="tdx:fixed tdx:inset-0 tdx:bg-black tdx:bg-opacity-90 tdx:flex tdx:items-center tdx:justify-center tdx:p-6"
            style={{ zIndex: 73 }}
          >
            <button
              ref={closeBtnRef}
              type="button"
              aria-label="Close"
              onClick={(e) => { e.stopPropagation(); handleClose() }}
              className="tdx:absolute tdx:top-4 tdx:right-4 tdx:z-10 tdx:text-white tdx:text-2xl tdx:leading-none tdx:w-10 tdx:h-10 tdx:flex tdx:items-center tdx:justify-center tdx:rounded-full tdx:bg-white/10 tdx:outline-none tdx:focus-visible:ring-2 tdx:focus-visible:ring-white/70"
            >
              &times;
            </button>
            <motion.img
              initial={{ scale: 0.92 }}
              animate={{ scale: 1 }}
              src={activeFrame.src}
              alt={activeFrame.alt}
              onClick={(e) => e.stopPropagation()}
              className="tdx:max-w-full tdx:max-h-full tdx:object-contain"
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
