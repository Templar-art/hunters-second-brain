import { createRoot } from "react-dom/client"
import { Component, StrictMode, type ReactNode } from "react"
import "./index.css"
import { ThreeDPhotoCarousel } from "./components/ui/carousel-3d"
import ProjectGallery from "./components/ui/image-gallery"
import PropertyShowcase from "./components/ui/property-showcase"
import { ALL_FRAMES } from "./data/project-frames"
import { SHOWCASE_PROPERTIES } from "./data/showcase-properties"

/* Two independent mount points, each a no-op if its container isn't on
   the page — this one bundle can sit on any page that opts in. */
const carouselRoot = document.getElementById("tdx-carousel-root")
if (carouselRoot) {
  createRoot(carouselRoot).render(
    <StrictMode>
      <ThreeDPhotoCarousel frames={ALL_FRAMES} />
    </StrictMode>
  )
}

const galleryRoot = document.getElementById("tdx-gallery-root")
if (galleryRoot) {
  createRoot(galleryRoot).render(
    <StrictMode>
      <ProjectGallery frames={ALL_FRAMES} />
    </StrictMode>
  )
}

class DebugErrorBoundary extends Component<
  { children: ReactNode; el: HTMLElement },
  { error: Error | null }
> {
  state = { error: null as Error | null }
  static getDerivedStateFromError(error: Error) {
    return { error }
  }
  componentDidCatch(error: Error) {
    this.props.el.setAttribute("data-mount-error", String(error?.stack || error))
  }
  render() {
    if (this.state.error) return null
    return this.props.children
  }
}

const showcaseRoot = document.getElementById("tdx-showcase-root")
if (showcaseRoot) {
  createRoot(showcaseRoot).render(
    <StrictMode>
      <DebugErrorBoundary el={showcaseRoot}>
        <PropertyShowcase properties={SHOWCASE_PROPERTIES} />
      </DebugErrorBoundary>
    </StrictMode>
  )
}
