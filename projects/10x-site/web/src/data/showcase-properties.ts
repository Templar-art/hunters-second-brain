export type ShowcaseProperty = {
  id: string
  name: string
  status: "Sold" | "For Sale"
  location: string
  blurb: string
  stats: { label: string; value: string }[]
  cover: string
  gallery: string[]
  film?: string
}

const base = "assets/showcase"

export const SHOWCASE_PROPERTIES: ShowcaseProperty[] = [
  {
    id: "boulevard",
    name: "The Boulevard",
    status: "Sold",
    location: "Riverfront Enclave",
    blurb:
      "A striking waterfront residence in a tightly held riverside enclave. Captured at golden hour from the air, with light-filled indoor to outdoor living at its heart.",
    stats: [
      { label: "Bed", value: "4" },
      { label: "Bath", value: "3" },
      { label: "Car", value: "2" },
      { label: "Frontage", value: "River" },
    ],
    cover: `${base}/boulevard/boulevard-01.jpg`,
    gallery: [
      `${base}/boulevard/boulevard-06.jpg`,
      `${base}/boulevard/boulevard-08.jpg`,
      `${base}/boulevard/boulevard-10.jpg`,
    ],
  },
  {
    id: "cairngorm",
    name: "11 Cairngorm Street",
    status: "Sold",
    location: "Family Residence",
    blurb:
      "A light-filled, two-storey family home framed by established gardens. Styled, photographed at golden hour, and taken to market at its full potential.",
    stats: [
      { label: "Bed", value: "4" },
      { label: "Bath", value: "2" },
      { label: "Car", value: "2" },
      { label: "To Sold", value: "14d" },
    ],
    cover: `${base}/cairngorm/cairngorm-01.jpg`,
    gallery: [
      `${base}/cairngorm/cairngorm-05.jpg`,
      `${base}/cairngorm/cairngorm-08.jpg`,
      `${base}/cairngorm/cairngorm-13.jpg`,
    ],
  },
  {
    id: "northview",
    name: "43 Northview",
    status: "For Sale",
    location: "Marina Frontage",
    blurb:
      "A waterfront position on the marina, presented from the ground and the air to tell the full story of the home and its setting.",
    stats: [
      { label: "Bed", value: "5" },
      { label: "Bath", value: "3" },
      { label: "Car", value: "2" },
      { label: "Frontage", value: "Water" },
    ],
    cover: `${base}/northview/northview-01.jpg`,
    gallery: [
      `${base}/northview/northview-04.jpg`,
      `${base}/northview/northview-20.jpg`,
      `${base}/northview/northview-25.jpg`,
    ],
    film: `${base}/northview-film.mp4`,
  },
]
