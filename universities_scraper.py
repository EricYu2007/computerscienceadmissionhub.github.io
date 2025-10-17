import json
import re
import requests
from bs4 import BeautifulSoup

universities_data = [
    {
        "name": "University of Oxford",
        "aLevels": "A*AA (A* in Maths/FM/CS required)",
        "ib": "40-42 points with 7,6,6 at HL (Maths HL required)",
        "admissionTest": "MAT",
        "fees": "£39,010",
        "location": "Oxford, England",
        "language": "IELTS 7.5 (minimum 7.0 in each component)",
    },
    {
        "name": "University of Cambridge",
        "aLevels": "A*A*A (Maths required; FM highly recommended)",
        "ib": "40-42 points with 7,7,6 at HL (Maths HL required)",
        "admissionTest": "TMUA",
        "fees": "£37,293",
        "location": "Cambridge, England",
        "language": "IELTS 7.5 (minimum 7.0 in each component)",
    },
    {
        "name": "Imperial College London",
        "aLevels": "A*A*A to A*AA (A* in Maths)",
        "ib": "40-42 points with 7,6,6 at HL (Maths HL required)",
        "admissionTest": "TMUA",
        "fees": "£35,100",
        "location": "London, England",
        "language": "IELTS 7.0 (minimum 6.5 in each component)",
    },
    {
        "name": "University of St Andrews",
        "aLevels": "AAA",
        "ib": "38 points with 6,6,6 HL including Maths",
        "admissionTest": "None",
        "fees": "£23,800",
        "location": "St Andrews, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Birmingham",
        "aLevels": "AAA-AAB",
        "ib": "36 points overall with 6 in HL Maths",
        "admissionTest": "None",
        "fees": "£32,100",
        "location": "Birmingham, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Bath",
        "aLevels": "A*AA-AAA",
        "ib": "36-37 points overall with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,900",
        "location": "Bath, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Warwick",
        "aLevels": "AAA",
        "ib": "38 points with 6 HL Maths",
        "admissionTest": "TMUA",
        "fees": "£26,700",
        "location": "Coventry, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Bristol",
        "aLevels": "AAA-AAB",
        "ib": "36 points overall with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£27,000",
        "location": "Bristol, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Manchester",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 in HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Manchester, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "King's College London",
        "aLevels": "AAA-AAB",
        "ib": "35-36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£27,000",
        "location": "London, England",
        "language": "IELTS 7.0 (minimum 6.5 in each component)",
    },
    {
        "name": "Durham University",
        "aLevels": "AAA",
        "ib": "38 points overall with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Durham, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "UCL (University College London)",
        "aLevels": "A*A*A-AAA",
        "ib": "39 points with 19-20 HL, including 6 in HL Maths",
        "admissionTest": "TARA",
        "fees": "£28,000",
        "location": "London, England",
        "language": "IELTS 7.0 (minimum 6.5 in each component)",
    },
    {
        "name": "University of Sheffield",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Sheffield, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Southampton",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Southampton, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Glasgow",
        "aLevels": "AAA-AAB",
        "ib": "38 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Glasgow, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "The University of Edinburgh",
        "aLevels": "AAA",
        "ib": "37-40 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Edinburgh, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of York",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "York, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Exeter",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Exeter, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Nottingham",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Nottingham, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Loughborough University",
        "aLevels": "AAA-AAB",
        "ib": "35 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Loughborough, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Lancaster University",
        "aLevels": "AAA-AAB",
        "ib": "36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£24,000",
        "location": "Lancaster, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Leeds",
        "aLevels": "AAA-AAB",
        "ib": "35-36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£26,500",
        "location": "Leeds, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Queen's University Belfast",
        "aLevels": "AAA-AAB",
        "ib": "34 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£22,000",
        "location": "Belfast, Northern Ireland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Royal Holloway",
        "aLevels": "AAB",
        "ib": "32 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£23,500",
        "location": "London, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Cardiff University",
        "aLevels": "AAA-AAB",
        "ib": "34-36 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£24,500",
        "location": "Cardiff, Wales",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Newcastle University",
        "aLevels": "AAA-AAB",
        "ib": "35 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Newcastle, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Queen Mary University of London",
        "aLevels": "AAB",
        "ib": "34 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£26,000",
        "location": "London, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Liverpool",
        "aLevels": "AAA-AAB",
        "ib": "35 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£24,000",
        "location": "Liverpool, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Surrey",
        "aLevels": "AAB",
        "ib": "34 points with 6 HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "Guildford, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Dundee",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£22,000",
        "location": "Dundee, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Strathclyde",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£23,000",
        "location": "Glasgow, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Swansea University",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£21,000",
        "location": "Swansea, Wales",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Heriot-Watt University",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£22,500",
        "location": "Edinburgh, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Sussex",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£24,500",
        "location": "Brighton, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Reading",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£23,500",
        "location": "Reading, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Leicester",
        "aLevels": "ABB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£22,500",
        "location": "Leicester, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Aston University",
        "aLevels": "BBB",
        "ib": "30-32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£23,000",
        "location": "Birmingham, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of East Anglia UEA",
        "aLevels": "BBB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£24,000",
        "location": "Norwich, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "City St George's",
        "aLevels": "BBB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "London, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Aberystwyth University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "Aberystwyth, Wales",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Kent",
        "aLevels": "BBB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£23,000",
        "location": "Canterbury, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Aberdeen",
        "aLevels": "BBB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£22,000",
        "location": "Aberdeen, Scotland",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Bangor University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Bangor, Wales",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Lincoln",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Lincoln, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Ulster University",
        "aLevels": "BBB",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£18,000",
        "location": "Belfast, Northern Ireland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Essex",
        "aLevels": "BBB",
        "ib": "30-32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£22,500",
        "location": "Colchester, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Bath Spa University",
        "aLevels": "BBC",
        "ib": "26 points (with HL Maths/CS/Physics)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Bath, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Brunel University of London",
        "aLevels": "BBB",
        "ib": "30-32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£24,000",
        "location": "London, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Stirling",
        "aLevels": "BBB",
        "ib": "28-30 points with HL Maths",
        "admissionTest": "None",
        "fees": "£20,500",
        "location": "Stirling, Scotland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Northumbria University",
        "aLevels": "BBC",
        "ib": "28-30 points with HL Maths",
        "admissionTest": "None",
        "fees": "£20,000",
        "location": "Newcastle, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Bristol, UWE",
        "aLevels": "AAB",
        "ib": "34 points with 6,5,5 at HL",
        "admissionTest": "None",
        "fees": "£27,000",
        "location": "Bristol, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "Manchester Metropolitan University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£20,000",
        "location": "Manchester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Nottingham Trent University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Nottingham, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Portsmouth",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£20,500",
        "location": "Portsmouth, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Abertay University",
        "aLevels": "BCC",
        "ib": "26 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£17,000",
        "location": "Dundee, Scotland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Glasgow Caledonian University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Glasgow, Scotland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Huddersfield",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "Huddersfield, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Winchester",
        "aLevels": "BBC",
        "ib": "28 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Winchester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Oxford Brookes University",
        "aLevels": "BBC",
        "ib": "29 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£20,000",
        "location": "Oxford, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Hull",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "Hull, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Bradford",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Bradford, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Edge Hill University",
        "aLevels": "BCC",
        "ib": "26 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£18,000",
        "location": "Ormskirk, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Worcester",
        "aLevels": "CCC",
        "ib": "24-26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Worcester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Keele University",
        "aLevels": "BBB",
        "ib": "30 points with HL Maths",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Keele, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Hertfordshire",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£20,000",
        "location": "Hatfield, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Kingston University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£20,500",
        "location": "Kingston, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Bournemouth University",
        "aLevels": "BBC",
        "ib": "28 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Bournemouth, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Staffordshire",
        "aLevels": "BCC",
        "ib": "26 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Stoke-on-Trent, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Robert Gordon University",
        "aLevels": "BBB",
        "ib": "30 points with HL Maths",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "Aberdeen, Scotland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Birmingham City University",
        "aLevels": "CCC",
        "ib": "24-26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Birmingham, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Edinburgh Napier University",
        "aLevels": "BBC",
        "ib": "28 points with HL Maths",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Edinburgh, Scotland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Leeds Beckett University",
        "aLevels": "BCC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "Leeds, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Liverpool John Moores University",
        "aLevels": "BCC",
        "ib": "26 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Liverpool, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Brighton",
        "aLevels": "BCC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£20,000",
        "location": "Brighton, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "London South Bank University",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£20,500",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Leeds Trinity University",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Leeds, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of the Arts London",
        "aLevels": "Varies",
        "ib": "Varies",
        "admissionTest": "None",
        "fees": "£25,000",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Sheffield Hallam University",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Sheffield, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Plymouth",
        "aLevels": "BBB",
        "ib": "30 points with HL Maths",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "Plymouth, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of South Wales",
        "aLevels": "CCC",
        "ib": "24-26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£18,500",
        "location": "Cardiff, Wales",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Falmouth University",
        "aLevels": "BCC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Falmouth, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Buckingham",
        "aLevels": "AAB-ABB",
        "ib": "34-35 points with HL Maths",
        "admissionTest": "None",
        "fees": "£28,000",
        "location": "Buckingham, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of Salford",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,500",
        "location": "Salford, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Coventry University",
        "aLevels": "BBB",
        "ib": "28-30 points with HL Maths",
        "admissionTest": "None",
        "fees": "£20,000",
        "location": "Coventry, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Derby",
        "aLevels": "BBC",
        "ib": "26-28 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£14,900",
        "location": "Derby, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "De Montfort University",
        "aLevels": "BBC",
        "ib": "28 points with HL Maths",
        "admissionTest": "None",
        "fees": "£16,000",
        "location": "Leicester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Teesside University",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£17,000",
        "location": "Middlesbrough, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Greenwich",
        "aLevels": "BCC",
        "ib": "26 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£18,000",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "York St John University",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£17,500",
        "location": "York, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Goldsmiths, University of London",
        "aLevels": "BBB",
        "ib": "32 points with HL Maths",
        "admissionTest": "None",
        "fees": "£22,000",
        "location": "London, England",
        "language": "IELTS 6.5 (minimum 6.0 in each component)",
    },
    {
        "name": "University of West London",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Sunderland",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,000",
        "location": "Sunderland, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Cardiff Metropolitan University",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£17,500",
        "location": "Cardiff, Wales",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Chichester",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "Chichester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Westminster",
        "aLevels": "BBC",
        "ib": "28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£19,000",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Chester",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£17,000",
        "location": "Chester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of East London",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Lancashire",
        "aLevels": "CCC",
        "ib": "24-28 points (HL Maths recommended)",
        "admissionTest": "None",
        "fees": "£17,500",
        "location": "Preston, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Gloucestershire",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,000",
        "location": "Gloucestershire, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Canterbury Christ Church University",
        "aLevels": "CCD",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "Canterbury, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Liverpool Hope University",
        "aLevels": "BCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£14,500",
        "location": "Liverpool, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Northampton",
        "aLevels": "BCC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,200",
        "location": "Northampton, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Anglia Ruskin University",
        "aLevels": "BCC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£18,800",
        "location": "Cambridge, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Bedfordshire",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "Luton, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of the West of Scotland",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,500",
        "location": "Paisley, Scotland",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Greater Manchester",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,950",
        "location": "Manchester, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Southampton Solent University",
        "aLevels": "BBC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,000",
        "location": "Southampton, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Norwich University of the Arts",
        "aLevels": "BCC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "Norwich, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Suffolk",
        "aLevels": "BBC",
        "ib": "26 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,000",
        "location": "Suffolk, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Middlesex University",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,600",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "London Metropolitan University",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,000",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Wolverhampton",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£15,525",
        "location": "Wolverhampton, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Wrexham University",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£11,750",
        "location": "Wrexham, Wales",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Wales Trinity Saint David",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,300",
        "location": "Carmarthen, Wales",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "Buckinghamshire New University",
        "aLevels": "CCD",
        "ib": "22 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "High Wycombe, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University for the Creative Arts",
        "aLevels": "BBC",
        "ib": "27 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,000",
        "location": "Farnham, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    },
    {
        "name": "University of Roehampton",
        "aLevels": "CCC",
        "ib": "24 points (Maths optional)",
        "admissionTest": "None",
        "fees": "£16,500",
        "location": "London, England",
        "language": "IELTS 6.0 (minimum 5.5 in each component)",
    }
]

def universities_rankings():
    """Scrape university rankings from the website using requests + BeautifulSoup"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        url = "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings/computer-science"
        
        print(f"Fetching data from: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try multiple possible selectors for the university names
        selectors = [
            ".swiper-slide.uni_nam.lt_list2",
            ".uni_nam",
            ".lt_list2",
            "[class*='uni_nam']",
            ".league-table-inner .uni-name",
            ".uni-name",
            ".institution-name"
        ]
        
        university_elements = None
        for selector in selectors:
            university_elements = soup.select(selector)
            if university_elements:
                print(f"Found {len(university_elements)} elements with selector: {selector}")
                break
        
        if not university_elements:
            print("No university elements found with any selector")
            # Try alternative approach - look for any elements that might contain university names
            all_elements = soup.find_all(text=re.compile(r'[Uu]niversity|[Cc]ollege'))
            if all_elements:
                print(f"Found {len(all_elements)} elements with university/college keywords")
                university_elements = all_elements
            else:
                return []
        
        # Get text from ALL elements, not just first 2
        universities = []
        for element in university_elements:  # Removed [:2] limit
            if hasattr(element, 'get_text'):
                text = element.get_text(strip=False)
            else:
                text = str(element)
            
            if text and len(text.strip()) > 3:
                # Split by newlines and add all parts
                parts = text.split('\n')
                for part in parts:
                    clean_part = part.strip()
                    if clean_part and len(clean_part) > 3:
                        universities.append(clean_part)
        
        print(f"Raw scraped data: {len(universities)} items")
        
        # More lenient filtering - only remove obviously invalid content
        filtered_universities = []
        for content in universities:
            content_clean = content.strip()
            
            # Skip if empty or too short
            if not content_clean or len(content_clean) < 3:
                continue
                
            # Skip if it's obviously not a university name
            content_lower = content_clean.lower()
            
            # Only filter out content that's CLEARLY not a university
            clearly_invalid = any(
                pattern in content_lower for pattern in [
                    'book open day', 'view courses', 'get prospectus', 
                    'apply now', 'book now', 'rank:', 'position:',
                    'open day', 'prospectus'
                ]
            )
            
            if clearly_invalid:
                continue
                
            # Skip if it's mostly numbers
            if content_clean.replace(' ', '').isdigit():
                continue
                
            filtered_universities.append(content_clean)
        
        # More lenient processing
        processed_universities = []
        for uni in filtered_universities:
            processed = clean_university_name(uni)
            
            if processed and len(processed) >= 3:
                # Final check - much more lenient than before
                words = processed.split()
                if (len(words) >= 1 and  # Single word names are okay
                    not any(bad in processed.lower() for bad in ['book ', 'view ', 'get ']) and
                    not processed.isdigit()):
                    processed_universities.append(processed)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_universities = []
        for uni in processed_universities:
            if uni not in seen:
                seen.add(uni)
                unique_universities.append(uni)
        
        print(f"Found {len(unique_universities)} valid universities after processing")
        
        # DEBUG: Print what we found
        if unique_universities:
            print("First 10 universities:", unique_universities[:10])
            print("Last 10 universities:", unique_universities[-10:])
        
        return unique_universities  # Return all
    
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return []

def clean_university_name(name):
    """Clean and normalize university name"""
    if not name:
        return None
    
    # Remove common suffixes and cleaning indicators
    patterns_to_remove = [
        r'\buniversity name\b',
        r'\bIN CLEARING\b',
        r'\bBOOK OPEN DAY\b', 
        r'\bVIEW COURSES\b',
        r'\bGET PROSPECTUS\b',
        r'\s*\.{3,}\s*',  # Remove ellipsis
    ]
    
    cleaned = name
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove content after comma but be careful - only if there's substantial text before
    comma_index = cleaned.find(",")
    if comma_index != -1 and comma_index > 10:  # Only if there's substantial text before comma
        cleaned = cleaned[:comma_index].strip()
    
    # Remove extra whitespace and normalize
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

def match_universities_with_data():
    """CORRECTED: Match scraped university names with our data"""
    scraped_names = universities_rankings()
    
    print(f"Scraped {len(scraped_names)} university names")
    if scraped_names:
        print("First 10 scraped names:", scraped_names[:10])
    
    # Remove "University name" header if present
    if scraped_names and scraped_names[0].lower() == 'university name':
        print("Removing 'University name' header")
        scraped_names = scraped_names[1:]
    
    # Create a lookup dictionary for exact matching
    hardcoded_lookup = {}
    for uni in universities_data:
        # Store with lowercase key for case-insensitive matching
        hardcoded_lookup[uni["name"].lower()] = uni
    
    matched_universities = []
    
    for scraped_name in scraped_names:
        scraped_lower = scraped_name.lower()
        found_match = None
        
        # Strategy 1: Exact match
        if scraped_lower in hardcoded_lookup:
            candidate = hardcoded_lookup[scraped_lower]
            if candidate not in matched_universities:
                found_match = candidate
        
        # Strategy 2: Try to find the best matching hardcoded university
        if not found_match:
            best_match = None
            best_score = 0
            
            for hardcoded_uni in universities_data:
                if hardcoded_uni in matched_universities:
                    continue  # Skip already used universities
                
                hardcoded_lower = hardcoded_uni["name"].lower()
                
                # Calculate similarity score
                score = calculate_similarity_score(scraped_lower, hardcoded_lower)
                
                if score > best_score and score > 0.7:  # Only good matches
                    best_score = score
                    best_match = hardcoded_uni
            
            if best_match:
                found_match = best_match
        
        if found_match:
            matched_universities.append(found_match)
            print(f"✅ CORRECT MATCH: '{scraped_name}' -> '{found_match['name']}'")
        else:
            # Create basic entry for universities not in hardcoded data
            basic_uni = {
                "name": scraped_name,
                "aLevels": "Check university website",
                "ib": "Check university website", 
                "admissionTest": "None",
                "fees": "Check university website",
                "location": "UK",
                "language": "Check university website"
            }
            matched_universities.append(basic_uni)
            print(f"❌ NO MATCH: '{scraped_name}' - created basic entry")
    
    print(f"\n--- SUMMARY ---")
    print(f"Total scraped universities: {len(scraped_names)}")
    print(f"Successfully matched with hardcoded data: {len([u for u in matched_universities if 'Check university website' not in u['aLevels']])}")
    print(f"Created basic entries: {len([u for u in matched_universities if 'Check university website' in u['aLevels']])}")
    
    return matched_universities

def calculate_similarity_score(name1, name2):
    """Calculate similarity between two university names"""
    # Exact match
    if name1 == name2:
        return 1.0
    
    # One contains the other (most common case)
    if name1 in name2 or name2 in name1:
        return 0.9
    
    # Handle common abbreviations
    abbreviations = {
        'ucl': 'university college london',
        'kcl': "king's college london", 
        'ic': 'imperial college',
        'rhul': 'royal holloway',
        'qmul': 'queen mary university of london'
    }
    
    for abbrev, full in abbreviations.items():
        if (name1 == abbrev and full in name2) or (name2 == abbrev and full in name1):
            return 0.85
    
    # Word overlap
    words1 = set(name1.split())
    words2 = set(name2.split())
    
    if words1 and words2:
        common_words = words1.intersection(words2)
        if common_words:
            return len(common_words) / max(len(words1), len(words2))
    
    return 0.0

def generate_university_json():
    """Generate the universities JSON file"""
    try:
        print("Starting university data scraping...")
        matched_universities = match_universities_with_data()
        universities_ranking = universities_rankings()
        
        print(f"Successfully matched {len(matched_universities)} universities")
        
        if not matched_universities:
            print("No universities matched. Using fallback data...")
            # Fallback: use first 50 universities from our data
            matched_universities = universities_data[:50]
        
        # Save to JSON file
        with open("universities.json", "w", encoding="utf-8") as f:
            json.dump(matched_universities, f, indent=2, ensure_ascii=False)
        with open("universities-name.json", "w",encoding="utf-8") as f:
            json.dump(universities_ranking, f, indent=2, ensure_ascii=False)
        
        print("✅ universities.json generated successfully!")
        
        # Print sample of saved data
        if matched_universities:
            print(f"First 5 universities saved: {[uni['name'] for uni in matched_universities[:5]]}")
        
        return matched_universities
        
    except Exception as error:
        print(f"Error generating JSON: {error}")
        # Create a fallback JSON file
        fallback_data = universities_data[:30]
        with open("universities.json", "w", encoding="utf-8") as f:
            json.dump(fallback_data, f, indent=2, ensure_ascii=False)
        print("✅ Fallback universities.json generated with sample data!")
        return fallback_data

if __name__ == "__main__":
    generate_university_json()
