/* eslint-disable object-shorthand */
import type { Locale, Messages } from "..";

/**
 * Statically load all the pre-localized dictionaries from the ./locales directory.
 *
 * NOTE: This process isn't automatic. To add a new static locale, follow these steps:
 * 1) Add the static import of the new ./{locale}/messages.json file
 * 2) Add the locale to the LOCALES object below
 */
import ar from "./ar/messages.json";
import bg from "./bg/messages.json";
import bs from "./bs/messages.json";
import ca from "./ca/messages.json";
import cs from "./cs/messages.json";
import da from "./da/messages.json";
import de from "./de/messages.json";
import el from "./el/messages.json";
import en from "./en/messages.json";
import es from "./es/messages.json";
import esMX from "./es-MX/messages.json";
import et from "./et/messages.json";
import eu from "./eu/messages.json";
import fi from "./fi/messages.json";
import fr from "./fr/messages.json";
import frCA from "./fr-CA/messages.json";
import gl from "./gl/messages.json";
import hiIN from "./hi-IN/messages.json";
import hr from "./hr/messages.json";
import hu from "./hu/messages.json";
import it from "./it/messages.json";
import ja from "./ja/messages.json";
import lt from "./lt/messages.json";
import lv from "./lv/messages.json";
import mt from "./mt/messages.json";
import nl from "./nl/messages.json";
import no from "./no/messages.json";
import pl from "./pl/messages.json";
import ptBR from "./pt-BR/messages.json";
import ptPT from "./pt-PT/messages.json";
import ro from "./ro/messages.json";
import ru from "./ru/messages.json";
import sk from "./sk/messages.json";
import sl from "./sl/messages.json";
import srCyrl from "./sr-Cyrl/messages.json";
import srLatn from "./sr-Latn/messages.json";
import sv from "./sv/messages.json";
import tr from "./tr/messages.json";
import uk from "./uk/messages.json";
import zh from "./zh/messages.json";

export const STATIC_MESSAGES: Record<Locale, Messages> = {
  ar: ar,
  bg: bg,
  bs: bs,
  ca: ca,
  cs: cs,
  da: da,
  de: de,
  el: el,
  en: en,
  es: es,
  "es-MX": esMX,
  et: et,
  eu: eu,
  fi: fi,
  fr: fr,
  "fr-CA": frCA,
  gl: gl,
  "hi-IN": hiIN,
  hr: hr,
  hu: hu,
  it: it,
  ja: ja,
  lt: lt,
  lv: lv,
  mt: mt,
  nl: nl,
  no: no,
  pl: pl,
  "pt-BR": ptBR,
  "pt-PT": ptPT,
  ro: ro,
  ru: ru,
  sk: sk,
  sl: sl,
  "sr-Cyrl": srCyrl,
  "sr-Latn": srLatn,
  sv: sv,
  tr: tr,
  uk: uk,
  zh: zh,
};
