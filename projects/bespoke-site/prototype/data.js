/* ==========================================================================
   BESPOKE — prototype seed data
   Shapes match BUILD-SPEC §4 exactly. In production this array is replaced by
   a Payload query (Path A) or a WP REST response (Path B); nothing else changes.
   Property photos are the client's placeholder set (47 Somerset Dr) reused across
   listings — swapped for real per-property media later. Suburbs/addresses illustrative.
   ========================================================================== */
(function (w) {
  var U = "https://bespoke.agents.10xvisuals.co/wp-content/uploads/2026/07/";
  var IMG = {
    drone2: U + "47-Somersert-Drive-_-Print-Drone-2-scaled.jpg",
    drone3: U + "47-Somersert-Drive-_-Print-Drone-3-scaled.jpg",
    i7: U + "47-Somersert-Drive-_-Print-7-scaled.jpg",
    i8: U + "47-Somersert-Drive-_-Print-8-scaled.jpg",
    i10: U + "47-Somersert-Drive-_-Print-10-scaled.jpg",
    i15: U + "47-Somersert-Drive-_-Print-15-scaled.jpg",
    i17: U + "47-Somersert-Drive-_-Print-17-scaled.jpg",
    i18: U + "47-Somersert-Drive-_-Print-18-scaled.jpg",
    i22: U + "47-Somersert-Drive-_-Print-22-scaled.jpg",
    i25: U + "47-Somersert-Drive-_-Print-25-scaled.jpg",
    i26: U + "47-Somersert-Drive-_-Print-26-scaled.jpg",
    i27: U + "47-Somersert-Drive-_-Print-27-scaled.jpg",
    i33: U + "47-Somersert-Drive-_-Print-33-scaled.jpg",
    t1: U + "47-Somerset-Drive-_-Touch-Ups-Print-scaled.jpg",
    t2: U + "47-Somerset-Drive-_-Touch-Ups-Print-2-scaled.jpg",
    t3: U + "47-Somerset-Drive-_-Touch-Ups-Print-3-scaled.jpg",
    t5: U + "47-Somerset-Drive-_-Touch-Ups-Print-5-scaled.jpg"
  };
  var TEAM = "../assets/img/team-ward.jpg";

  var AGENTS = {
    jason:   { id:"a1", slug:"jason-ward",   name:"Jason Ward",   role:"Principal Agent", photo:{url:TEAM,alt:"Jason Ward"},   phone:"0424 731 063", email:"jason@bespokerealestate.com.au" },
    barbara: { id:"a2", slug:"barbara-ward", name:"Barbara Ward", role:"Director",         photo:{url:TEAM,alt:"Barbara Ward"}, phone:"0424 731 063", email:"barbara@bespokerealestate.com.au" }
  };

  function media(url, alt){ return { url:url, alt:alt, type:"image" }; }

  var LISTINGS = [
    {
      id:"l1", slug:"12-the-sovereign-mile-sovereign-islands",
      address:{ street:"12 The Sovereign Mile", suburb:"sovereign-islands", state:"QLD", postcode:"4216" },
      status:"for_sale", propertyType:"house",
      price:{ display:"eoi", label:"Expressions of Interest closing 21 August" },
      beds:5, baths:6, cars:4, landSize:1012, floorSize:620,
      hero: media(IMG.drone2,"Waterfront residence, Sovereign Islands"),
      gallery:[IMG.i15,IMG.i25,IMG.i33,IMG.i7,IMG.t5,IMG.i27].map(function(u){return media(u,"Interior");}),
      video:null, floorplans:[],
      agent:"jason", coAgent:"barbara",
      description:["Set on a north-facing deep-water frontage, this is a residence composed with restraint. Volume, light and material do the talking, from the honed stone entry through to living spaces that open fully to the water.","The plan separates quiet from gathering. A primary wing sits apart from four further bedroom suites, while the kitchen, scullery and dining run as one uninterrupted line toward the pool terrace.","Held privately behind a gated approach, it offers the address, the aspect and the calm that Sovereign Islands is known for."],
      features:["North-facing deep-water frontage","Pontoon with ocean access","Honed stone and oak throughout","Gas heated pool and spa","Four-car garaging","Home cinema","Full home automation","Gated motor court"],
      soldData:null, externalId:null,
      seo:{ title:"12 The Sovereign Mile, Sovereign Islands", description:"Deep-water residence on Sovereign Islands." }
    },
    {
      id:"l2", slug:"8-cronin-avenue-mermaid-waters",
      address:{ street:"8 Cronin Avenue", suburb:"mermaid-waters", state:"QLD", postcode:"4218" },
      status:"for_sale", propertyType:"house",
      price:{ display:"numeric", amount:4250000 },
      beds:4, baths:3, cars:2, landSize:610, floorSize:340,
      hero: media(IMG.i15,"Living room, Mermaid Waters"),
      gallery:[IMG.i25,IMG.i33,IMG.i7,IMG.i8,IMG.i22,IMG.i26].map(function(u){return media(u,"Interior");}),
      video:null, floorplans:[],
      agent:"barbara", coAgent:null,
      description:["A considered single-level home on a wide waterfront block, walking distance to the beach. The interior is warm and unfussy, built around a central courtyard that draws light deep into the plan.","Living flows to a covered terrace and lap pool, with a separate media room and a study that could serve as a fourth bedroom.","Tightly held and rarely available in this pocket of Mermaid Waters."],
      features:["Wide waterfront block","Central light courtyard","Lap pool","Media room","Walk to beach","Double garage plus workshop"],
      soldData:null, externalId:null,
      seo:{ title:"8 Cronin Avenue, Mermaid Waters", description:"Single-level waterfront home, Mermaid Waters." }
    },
    {
      id:"l3", slug:"34-monaco-street-broadbeach-waters",
      address:{ street:"34 Monaco Street", suburb:"broadbeach-waters", state:"QLD", postcode:"4218" },
      status:"under_offer", propertyType:"house",
      price:{ display:"poa" },
      beds:5, baths:4, cars:3, landSize:720, floorSize:410,
      hero: media(IMG.i25,"Kitchen and dining, Broadbeach Waters"),
      gallery:[IMG.i33,IMG.i27,IMG.i18,IMG.i10,IMG.t2,IMG.i7].map(function(u){return media(u,"Interior");}),
      video:null, floorplans:[],
      agent:"jason", coAgent:null,
      description:["A generous family residence on a main-river-adjacent canal, presented in move-in condition. The ground floor is designed for entertaining, with a butler's pantry serving both the kitchen and the outdoor kitchen beyond.","Upstairs, four bedrooms open to a central retreat, with the primary suite taking the full water-facing width.","Central to Broadbeach dining and the beach, on one of the suburb's most established streets."],
      features:["Wide canal frontage","Butler's pantry","Outdoor kitchen","Upstairs retreat","Ducted climate control","Three-car garage"],
      soldData:null, externalId:null,
      seo:{ title:"34 Monaco Street, Broadbeach Waters", description:"Canal-front family residence, Broadbeach Waters." }
    },
    {
      id:"l4", slug:"5-como-crescent-isle-of-capri",
      address:{ street:"5 Como Crescent", suburb:"isle-of-capri", state:"QLD", postcode:"4217" },
      status:"sold", propertyType:"house",
      price:{ display:"contact_agent" },
      beds:4, baths:3, cars:2, landSize:600, floorSize:320,
      hero: media(IMG.i33,"Sold residence, Isle of Capri"),
      gallery:[IMG.i7,IMG.i15,IMG.i8,IMG.i22,IMG.i26,IMG.t3].map(function(u){return media(u,"Interior");}),
      video:null, floorplans:[],
      agent:"barbara", coAgent:"jason",
      description:["Sold prior to auction. A crisp contemporary home on a quiet Isle of Capri crescent, minutes from Surfers Paradise yet held apart from it.","Delivered a suburb record for the street on a considered, off-market campaign."],
      features:["Waterfront reserve outlook","Wine room","Heated pool","Off-market campaign"],
      soldData:{ date:"2026-05-14", price:3850000, suburbRecord:true }, externalId:null,
      seo:{ title:"5 Como Crescent, Isle of Capri", description:"Suburb record, Isle of Capri." }
    },
    {
      id:"l5", slug:"21-45-commodore-drive-paradise-waters",
      address:{ street:"2101 / 45 Commodore Drive", suburb:"paradise-waters", state:"QLD", postcode:"4217" },
      status:"upcoming", propertyType:"apartment",
      price:{ display:"contact_agent" },
      beds:3, baths:2, cars:2, landSize:null, floorSize:245,
      hero: media(IMG.i7,"Whole-floor apartment, Paradise Waters"),
      gallery:[IMG.i18,IMG.i27,IMG.i10,IMG.i25,IMG.t1,IMG.i17].map(function(u){return media(u,"Interior");}),
      video:null, floorplans:[],
      agent:"jason", coAgent:null,
      description:["A whole-floor residence in a boutique riverfront building, coming to market shortly. Broadwater and city views wrap two aspects, with a private lift landing and near-300sqm of single-level living.","Register your interest ahead of the first inspection."],
      features:["Whole-floor, single level","Private lift lobby","Dual river and city aspect","Secure basement parking","Concierge building"],
      soldData:null, externalId:null,
      seo:{ title:"2101 / 45 Commodore Drive, Paradise Waters", description:"Whole-floor riverfront apartment, Paradise Waters." }
    },
    {
      id:"l6", slug:"61-the-masthead-sanctuary-cove",
      address:{ street:"61 The Masthead", suburb:"sanctuary-cove", state:"QLD", postcode:"4212" },
      status:"sold", propertyType:"house",
      price:{ display:"contact_agent" },
      beds:5, baths:5, cars:4, landSize:1180, floorSize:660,
      hero: media(IMG.drone3,"Sold residence, Sanctuary Cove"),
      gallery:[IMG.i26,IMG.i22,IMG.i8,IMG.i15,IMG.i33,IMG.t5].map(function(u){return media(u,"Interior");}),
      video:null, floorplans:[],
      agent:"jason", coAgent:"barbara",
      description:["A resort-scale residence within the gates of Sanctuary Cove, sold following a targeted off-market approach to qualified buyers.","Deep-water berth, championship-golf surrounds and a floorplan built for both family and entertaining."],
      features:["Private marina berth","Gated golf community","Tennis court","Guest pavilion","Six-seat cinema"],
      soldData:{ date:"2026-03-02", price:6100000, suburbRecord:false }, externalId:null,
      seo:{ title:"61 The Masthead, Sanctuary Cove", description:"Resort residence, Sanctuary Cove." }
    }
  ];

  var REGIONS = [
    { id:"r1", slug:"sovereign-islands", name:"Sovereign Islands", tier:"primary", order:1,
      hero:media(IMG.drone2,"Sovereign Islands"),
      intro:"The Gold Coast's most exclusive address. A gated, man-made archipelago of deep-water estates where frontage, privacy and scale set the market. Sovereign Islands rewards buyers who want the very top of the market and the calm that comes with it." },
    { id:"r2", slug:"mermaid-waters", name:"Mermaid Waters", tier:"primary", order:2,
      hero:media(IMG.i15,"Mermaid Waters"),
      intro:"Blue-chip and beachside. Mermaid Waters pairs wide waterfront blocks with genuine walk-to-sand living, moments from Nobby Beach and the Hedges Avenue strip. A pocket that holds its value through every cycle." },
    { id:"r3", slug:"broadbeach-waters", name:"Broadbeach Waters", tier:"primary", order:3,
      hero:media(IMG.i25,"Broadbeach Waters"),
      intro:"Central, established and consistently in demand. Broadbeach Waters offers wide canals and generous family homes a short drive from Broadbeach dining and the beach. A suburb Bespoke knows street by street." },
    { id:"r4", slug:"paradise-waters", name:"Paradise Waters", tier:"primary", order:4,
      hero:media(IMG.i7,"Paradise Waters"),
      intro:"Tightly held riverfront living beside Main Beach. Paradise Waters is compact and rarely traded, prized for its Broadwater aspect and its proximity to Tedder Avenue and the spit." },
    { id:"r5", slug:"isle-of-capri", name:"Isle of Capri", tier:"primary", order:5,
      hero:media(IMG.i33,"Isle of Capri"),
      intro:"Island living beside Surfers Paradise, held apart from it. Isle of Capri is leafy, quiet and closely held, with a village heart and some of the most sought-after waterfront crescents on the coast." },
    { id:"r6", slug:"sanctuary-cove", name:"Sanctuary Cove", tier:"primary", order:6,
      hero:media(IMG.drone3,"Sanctuary Cove"),
      intro:"Gated, golf-and-marina resort living on the northern Gold Coast. Sanctuary Cove offers security, deep-water berths and a lifestyle community, a distinct market that suits a specific and discerning buyer." }
  ];

  w.BESPOKE_DATA = { LISTINGS: LISTINGS, REGIONS: REGIONS, AGENTS: AGENTS };
})(window);
