/* Adapted from the pasted reference: real 10x Visuals project photos
   instead of Unsplash stock, and no global font override — the host
   page already sets Prata/Montserrat site-wide (assets/prestige.css),
   and a bare `*{font-family:...}` rule here would have clobbered it. */
export default function ProjectGallery() {
  const frames = [
    { src: "assets/work-stonehaven-1400.jpg", alt: "Stonehaven, the front elevation at 47 Somerset Drive, symmetrical under a clear sky." },
    { src: "assets/work-bespoke-1400.jpg", alt: "A prestige Gold Coast listing photographed for Bespoke Estate Agents." },
    { src: "assets/work-davenport-1400.jpg", alt: "Davenport, a refined hillside residence marketed by PRD Burleigh, looking out over the pool." },
    { src: "assets/work-elysium-1400.jpg", alt: "Elysium, a completed large scale apartment development delivered by Shape Construction." },
    { src: "assets/work-sol-1400.jpg", alt: "SOL by Skye Development Group, the completed canal side compound lit at night." },
    { src: "assets/work-broncos-1400.jpg", alt: "The refurbished Broncos Leagues Club interior, delivered by Ashley Cooper Construction." },
  ]

  return (
    <section className="tdx:w-full tdx:flex tdx:flex-col tdx:items-center tdx:justify-start">
      <div className="tdx:flex tdx:items-center tdx:gap-2 tdx:h-[400px] tdx:w-full tdx:max-w-5xl tdx:px-4">
        {frames.map((frame, idx) => (
          <div
            key={idx}
            className="tdx:relative tdx:group tdx:flex-grow tdx:transition-all tdx:w-56 tdx:rounded-lg tdx:overflow-hidden tdx:h-[400px] tdx:duration-500 tdx:hover:w-full"
          >
            <img
              className="tdx:h-full tdx:w-full tdx:object-cover tdx:object-center"
              src={frame.src}
              alt={frame.alt}
            />
          </div>
        ))}
      </div>
    </section>
  )
}
