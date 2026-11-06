"""Every published figure Michaneer uses, with where it comes from.

Each threshold in model.py names its source id from this table, and the
Sources page renders the table as is. All entries were checked on
6 November 2026.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    id: str
    title: str
    publisher: str
    date: str
    url: str
    used_for: str
    note: str = ""


SOURCES: tuple[Source, ...] = (
    Source(
        id="is10500",
        title="IS 10500:2012 Drinking Water Specification (Second Revision), Table 2",
        publisher="Bureau of Indian Standards",
        date="2012",
        url="https://cpcb.nic.in/wqm/BIS_Drinking_Water_Specification.pdf",
        used_for=(
            "Total dissolved solids: 500 mg/L acceptable limit, 2000 mg/L "
            "permissible limit in the absence of an alternate source."
        ),
    ),
    Source(
        id="is16240",
        title="IS 16240:2023 Reverse Osmosis based Point-of-Use Water Treatment System",
        publisher="Bureau of Indian Standards",
        date="2023",
        url="https://www.bis.gov.in/wp-content/uploads/2025/07/PM-IS-16240-CMD2.pdf",
        used_for=(
            "Minimum recovery of 40 percent for domestic RO purifiers, raised "
            "from 20 percent in the 2015 edition. Recovery rating must be declared."
        ),
        note=(
            "The 40 percent figure is also restated in the CPCB draft and final "
            "reject-water guidelines (see cpcb2026)."
        ),
    ),
    Source(
        id="gsr724",
        title=(
            "G.S.R. 724(E), Environment (Protection) 115th Amendment Rules, 2021: "
            "Regulation on use of Water Purification System"
        ),
        publisher="Ministry of Environment, Forest and Climate Change, Gazette of India",
        date="4 October 2021",
        url="https://tnpcb.gov.in/PDF/Updates/Whats_New/GazetteNotificationOsmosisWPS1623.pdf",
        used_for=(
            "\"The user shall comply with the guidelines issued by CPCB for "
            "management, storage, utilisation and disposal of reject water\". "
            "Every domestic purifier label must show \"Rated recovery efficiency "
            "and corresponding water reject generation\". Water supply agencies "
            "must tell consumers the TDS of the water they supply."
        ),
    ),
    Source(
        id="cpcb2026",
        title=(
            "Guidelines for Handling, Storage, Management, Utilisation and Disposal "
            "of RO Reject Water and Discarded Elements"
        ),
        publisher="Central Pollution Control Board",
        date="23 September 2026 (draft of 20 January 2026, file A-14011/1/2026-WQM-I/21)",
        url=(
            "https://teamleaseregtech.com/updates/article/59799/"
            "cpcb-issued-the-guidelines-for-handling-storage-management-utilisation"
        ),
        used_for=(
            "Reject water should be reused to the maximum possible extent for "
            "non-potable purposes such as floor cleaning, vehicle washing and "
            "toilet flushing. Unused reject goes to the sewer."
        ),
        note="Summary by TeamLease RegTech; the CPCB PDF was not reachable from our network.",
    ),
    Source(
        id="loksabha778",
        title="Lok Sabha Unstarred Question No. 778, answered 17 September 2020",
        publisher="Ministry of Housing and Urban Affairs, Lok Sabha",
        date="17 September 2020",
        url="https://eparlib.sansad.in/bitstream/123456789/968054/1/AU778.pdf",
        used_for=(
            "\"The reject quantity varies between 1 to 3 litre per litre of "
            "permeate depending on the size and purpose of RO system.\" "
            "\"No such study has been carried out by the Ministry.\""
        ),
        note="Text as indexed by search; the Lok Sabha archive did not load from our network.",
    ),
    Source(
        id="ngt134",
        title="O.A. No. 134/2015, Friends v. Ministry of Water Resources",
        publisher="National Green Tribunal",
        date="Order of 20 May 2019; further order of 1 December 2021",
        url="https://www.greentribunal.gov.in/sites/default/files/all_documents/134-2015.pdf",
        used_for=(
            "Directed a ban on RO where TDS is below 500 mg/L and at least "
            "60 percent recovery where RO is allowed."
        ),
        note=(
            "The Supreme Court stayed paragraph 6 of the 1 December 2021 order "
            "in an appeal by the Water Quality India Association (reported "
            "1 March 2022). Michaneer treats the 60 percent figure as a stayed "
            "direction, not as law."
        ),
    ),
    Source(
        id="sc_stay",
        title="SC stays order of NGT directing CPCB to ban water purifiers with TDS below 500 mg/L",
        publisher="Verdictum",
        date="1 March 2022",
        url=(
            "https://www.verdictum.in/top-stories/"
            "sc-stays-order-of-ngt-directing-cpcb-to-ban-water-purifiers-with-tds-below-500-mgl-1357253"
        ),
        used_for="Status of the NGT direction: stayed until further orders.",
    ),
    Source(
        id="fao29",
        title="Water quality for agriculture, FAO Irrigation and Drainage Paper 29 Rev. 1, Table 1",
        publisher="Food and Agriculture Organization of the United Nations (Ayers and Westcot)",
        date="1985",
        url="https://www.fao.org/4/t0234e/T0234E01.htm",
        used_for=(
            "Salinity restriction on irrigation water by TDS: under 450 mg/L "
            "none, 450 to 2000 mg/L slight to moderate, over 2000 mg/L severe."
        ),
    ),
    Source(
        id="who2003",
        title="Domestic Water Quantity, Service Level and Health (WHO/SDE/WSH/03.02)",
        publisher="World Health Organization (Howard and Bartram)",
        date="2003",
        url="https://iris.who.int/handle/10665/67884",
        used_for=(
            "About 7.5 litres per person per day for drinking and food "
            "preparation. Used only as a hint beside an input the user can change."
        ),
    ),
)


def by_id(source_id: str) -> Source:
    for source in SOURCES:
        if source.id == source_id:
            return source
    raise KeyError(source_id)


SHORT = {
    "is10500": "BIS IS 10500",
    "is16240": "BIS IS 16240",
    "gsr724": "G.S.R. 724(E)",
    "cpcb2026": "CPCB guidelines 2026",
    "loksabha778": "Lok Sabha Q. 778",
    "ngt134": "NGT O.A. 134/2015",
    "sc_stay": "Supreme Court stay",
    "fao29": "FAO Paper 29",
    "who2003": "WHO 2003",
}
