import { createRoot } from "react-dom/client"
import { StrictMode } from "react"
import "./index.css"
import { ThreeDPhotoCarousel } from "./components/ui/carousel-3d"
import ProjectGallery from "./components/ui/image-gallery"

/* Two independent mount points, each a no-op if its container isn't on
   the page — this one bundle can sit on any page that opts in. */
const carouselRoot = document.getElementById("tdx-carousel-root")
if (carouselRoot) {
  createRoot(carouselRoot).render(
    <StrictMode>
      <ThreeDPhotoCarousel />
    </StrictMode>
  )
}

const galleryRoot = document.getElementById("tdx-gallery-root")
if (galleryRoot) {
  createRoot(galleryRoot).render(
    <StrictMode>
      <ProjectGallery />
    </StrictMode>
  )
}
