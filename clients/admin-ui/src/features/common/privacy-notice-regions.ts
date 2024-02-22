import { PrivacyNoticeRegion } from "~/types/api";

/**
 * A mapping of privacy notice regions to human readable names.
 *
 * The typing is important here so that our build will fail if we are missing a region.
 */
export const PRIVACY_NOTICE_REGION_RECORD: Record<PrivacyNoticeRegion, string> =
  {
    [PrivacyNoticeRegion.US]: "United States",
    [PrivacyNoticeRegion.US_AL]: "Alabama (USA)",
    [PrivacyNoticeRegion.US_AK]: "Alaska (USA)",
    [PrivacyNoticeRegion.US_AZ]: "Arizona (USA)",
    [PrivacyNoticeRegion.US_AR]: "Arkansas (USA)",
    [PrivacyNoticeRegion.US_CA]: "California (USA)",
    [PrivacyNoticeRegion.US_CO]: "Colorado (USA)",
    [PrivacyNoticeRegion.US_CT]: "Connecticut (USA)",
    [PrivacyNoticeRegion.US_DE]: "Delaware (USA)",
    [PrivacyNoticeRegion.US_FL]: "Florida (USA)",
    [PrivacyNoticeRegion.US_GA]: "Georgia (USA)",
    [PrivacyNoticeRegion.US_HI]: "Hawaii (USA)",
    [PrivacyNoticeRegion.US_ID]: "Idaho (USA)",
    [PrivacyNoticeRegion.US_IL]: "Illinois (USA)",
    [PrivacyNoticeRegion.US_IN]: "Indiana (USA)",
    [PrivacyNoticeRegion.US_IA]: "Iowa (USA)",
    [PrivacyNoticeRegion.US_KS]: "Kansas (USA)",
    [PrivacyNoticeRegion.US_KY]: "Kentucky (USA)",
    [PrivacyNoticeRegion.US_LA]: "Louisiana (USA)",
    [PrivacyNoticeRegion.US_ME]: "Maine (USA)",
    [PrivacyNoticeRegion.US_MD]: "Maryland (USA)",
    [PrivacyNoticeRegion.US_MA]: "Massachusetts (USA)",
    [PrivacyNoticeRegion.US_MI]: "Michigan (USA)",
    [PrivacyNoticeRegion.US_MN]: "Minnesota (USA)",
    [PrivacyNoticeRegion.US_MS]: "Mississippi (USA)",
    [PrivacyNoticeRegion.US_MO]: "Missouri (USA)",
    [PrivacyNoticeRegion.US_MT]: "Montana (USA)",
    [PrivacyNoticeRegion.US_NE]: "Nebraska (USA)",
    [PrivacyNoticeRegion.US_NV]: "Nevada (USA)",
    [PrivacyNoticeRegion.US_NH]: "New Hampshire (USA)",
    [PrivacyNoticeRegion.US_NJ]: "New Jersey (USA)",
    [PrivacyNoticeRegion.US_NM]: "New Mexico (USA)",
    [PrivacyNoticeRegion.US_NY]: "New York (USA)",
    [PrivacyNoticeRegion.US_NC]: "North Carolina (USA)",
    [PrivacyNoticeRegion.US_ND]: "North Dakota (USA)",
    [PrivacyNoticeRegion.US_OH]: "Ohio (USA)",
    [PrivacyNoticeRegion.US_OK]: "Oklahoma (USA)",
    [PrivacyNoticeRegion.US_OR]: "Oregon (USA)",
    [PrivacyNoticeRegion.US_PA]: "Pennsylvania (USA)",
    [PrivacyNoticeRegion.US_RI]: "Rhode Island (USA)",
    [PrivacyNoticeRegion.US_SC]: "South Carolina (USA)",
    [PrivacyNoticeRegion.US_SD]: "South Dakota (USA)",
    [PrivacyNoticeRegion.US_TN]: "Tennessee (USA)",
    [PrivacyNoticeRegion.US_TX]: "Texas (USA)",
    [PrivacyNoticeRegion.US_UT]: "Utah (USA)",
    [PrivacyNoticeRegion.US_VT]: "Vermont (USA)",
    [PrivacyNoticeRegion.US_VA]: "Virginia (USA)",
    [PrivacyNoticeRegion.US_WA]: "Washington (USA)",
    [PrivacyNoticeRegion.US_WV]: "West Virginia (USA)",
    [PrivacyNoticeRegion.US_WI]: "Wisconsin (USA)",
    [PrivacyNoticeRegion.US_WY]: "Wyoming (USA)",
    [PrivacyNoticeRegion.BE]: "Belgium (EU)",
    [PrivacyNoticeRegion.BG]: "Bulgaria (EU)",
    [PrivacyNoticeRegion.CZ]: "Czech Republic (EU)",
    [PrivacyNoticeRegion.DK]: "Denmark (EU)",
    [PrivacyNoticeRegion.DE]: "Germany (EU)",
    [PrivacyNoticeRegion.EE]: "Estonia (EU)",
    [PrivacyNoticeRegion.IE]: "Ireland (EU)",
    [PrivacyNoticeRegion.GR]: "Greece (EU)",
    [PrivacyNoticeRegion.ES]: "Spain (EU)",
    [PrivacyNoticeRegion.FR]: "France (EU)",
    [PrivacyNoticeRegion.HR]: "Croatia (EU)",
    [PrivacyNoticeRegion.IT]: "Italy (EU)",
    [PrivacyNoticeRegion.CY]: "Cyprus (EU)",
    [PrivacyNoticeRegion.LV]: "Latvia (EU)",
    [PrivacyNoticeRegion.LT]: "Lithuania (EU)",
    [PrivacyNoticeRegion.LU]: "Luxembourg (EU)",
    [PrivacyNoticeRegion.HU]: "Hungary (EU)",
    [PrivacyNoticeRegion.MT]: "Malta (EU)",
    [PrivacyNoticeRegion.NL]: "Netherlands (EU)",
    [PrivacyNoticeRegion.AT]: "Austria (EU)",
    [PrivacyNoticeRegion.PL]: "Poland (EU)",
    [PrivacyNoticeRegion.PT]: "Portugal (EU)",
    [PrivacyNoticeRegion.RO]: "Romania (EU)",
    [PrivacyNoticeRegion.SI]: "Slovenia (EU)",
    [PrivacyNoticeRegion.SK]: "Slovakia (EU)",
    [PrivacyNoticeRegion.FI]: "Finland (EU)",
    [PrivacyNoticeRegion.SE]: "Sweden (EU)",
    [PrivacyNoticeRegion.GB]: "Great Britain",
    [PrivacyNoticeRegion.GB_ENG]: "England",
    [PrivacyNoticeRegion.GB_SCT]: "Scotland",
    [PrivacyNoticeRegion.GB_WLS]: "Wales",
    [PrivacyNoticeRegion.GB_NIR]: "Northern Ireland",
    [PrivacyNoticeRegion.IS]: "Iceland",
    [PrivacyNoticeRegion.NO]: "Norway",
    [PrivacyNoticeRegion.LI]: "Liechtenstein",
    [PrivacyNoticeRegion.CA]: "Canada",
    [PrivacyNoticeRegion.CA_AB]: "Alberta (Canada)",
    [PrivacyNoticeRegion.CA_BC]: "British Columbia (Canada)",
    [PrivacyNoticeRegion.CA_MB]: "Manitoba (Canada)",
    [PrivacyNoticeRegion.CA_NB]: "New Brunswick (Canada)",
    [PrivacyNoticeRegion.CA_NL]: "Newfoundland and Labrador (Canada)",
    [PrivacyNoticeRegion.CA_NS]: "Nova Scotia (Canada)",
    [PrivacyNoticeRegion.CA_ON]: "Ontario (Canada)",
    [PrivacyNoticeRegion.CA_PE]: "Prince Edward Island (Canada)",
    [PrivacyNoticeRegion.CA_QC]: "Quebec (Canada)",
    [PrivacyNoticeRegion.CA_SK]: "Saskatchewan (Canada)",
    [PrivacyNoticeRegion.CA_NT]: "Northwest Territories (Canada)",
    [PrivacyNoticeRegion.CA_NU]: "Nunavut (Canada)",
    [PrivacyNoticeRegion.CA_YT]: "Yukon (Canada)",
    [PrivacyNoticeRegion.EEA]: "European Economic Area",
  };

export const PRIVACY_NOTICE_REGION_MAP = new Map(
  Object.entries(PRIVACY_NOTICE_REGION_RECORD)
);

export const PRIVACY_NOTICE_REGION_OPTIONS = Object.entries(
  PRIVACY_NOTICE_REGION_RECORD
).map((entry) => ({
  value: entry[0],
  label: entry[1],
}));
