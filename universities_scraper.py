import json
import re
import requests
from bs4 import BeautifulSoup
import time

# Your existing data
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
        "admissionTest": "None",
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
        "admissionTest": "None",
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
        "admissionTest": "None",
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
        "name": "University of Creative Arts",
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
            ".league-table-inner .uni-name"
        ]
        
        university_elements = None
        for selector in selectors:
            university_elements = soup.select(selector)
            if university_elements:
                print(f"Found elements with selector: {selector}")
                break
        
        if not university_elements:
            print("No university elements found with any selector")
            return []
        
        # Get text from elements
        universities = []
        for element in university_elements[:2]:  # Check first 2 elements like original JS
            text = element.get_text(strip=False)
            if text and len(text) > 10:
                universities.extend(text.split('\n'))
        
        # Define unwanted patterns to filter out
        unwanted_patterns = [
            'university name', 'book open day', 'view courses', 'get prospectus',
            'in clearing', 'clearing', 'open day', 'book now', 'apply now',
            'rank', 'ranking', 'position'
        ]
        
        # Filter universities more aggressively
        filtered_universities = []
        for content in universities:
            content_clean = content.strip()
            
            # Skip if empty or too short
            if not content_clean or len(content_clean) < 5:
                continue
                
            # Skip if it's obviously not a university name
            content_lower = content_clean.lower()
            if any(unwanted in content_lower for unwanted in unwanted_patterns):
                continue
                
            # Skip if it's mostly numbers or special characters
            if content_clean.isdigit():
                continue
                
            # Skip common non-university text patterns
            if (content_lower.startswith('book ') or 
                content_lower.startswith('view ') or 
                content_lower.startswith('get ') or
                'open day' in content_lower or
                'prospectus' in content_lower):
                continue
                
            filtered_universities.append(content_clean)
        
        # Process university names
        processed_universities = []
        for uni in filtered_universities:
            processed = uni.strip()
            
            # Remove common prefixes/suffixes and clean up
            processed = re.sub(r'\bIN CLEARING\b', '', processed, flags=re.IGNORECASE).strip()
            processed = re.sub(r'\bBOOK OPEN DAY\b', '', processed, flags=re.IGNORECASE).strip()
            processed = re.sub(r'\bVIEW COURSES\b', '', processed, flags=re.IGNORECASE).strip()
            processed = re.sub(r'\bGET PROSPECTUS\b', '', processed, flags=re.IGNORECASE).strip()
            
            # Remove content after comma (like in original JS)
            comma_index = processed.find(",")
            if comma_index != -1:
                processed = processed[:comma_index].strip()
            
            # Remove ellipsis and clean up
            processed = re.sub(r'\.{3,}', '', processed).strip()
            
            # Normalize whitespace
            processed = re.sub(r'\s+', ' ', processed)
            
            # Final validation - must look like a university name
            if (len(processed) > 5 and 
                not processed.isdigit() and
                not any(unwanted in processed.lower() for unwanted in unwanted_patterns) and
                ('university' in processed.lower() or 'college' in processed.lower() or processed.count(' ') >= 1)):
                processed_universities.append(processed)
        
        print(f"Found {len(processed_universities)} valid universities after processing")
        if processed_universities:
            print("Sample processed universities:", processed_universities[:10])
        
        return processed_universities[:100]
    
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

def match_universities_with_data():
    """Match scraped university names with our data"""
    scraped_names = universities_rankings()
    matched_universities = []
    
    print(f"Scraped {len(scraped_names)} university names")
    if scraped_names:
        print("First 10 scraped names:", scraped_names[:10])
    
    # Handle truncated names (like 'University of Wales Trinity Saint D...')
    def normalize_name(name):
        name = re.sub(r'\.{3,}', '', name)  # Remove ellipsis
        name = re.sub(r'\s+', ' ', name).strip()
        return name
    
    # More flexible matching
    for uni_name in scraped_names:
        normalized_scraped = normalize_name(uni_name)
        found = False
        
        for uni_data in universities_data:
            normalized_data = normalize_name(uni_data["name"])
            
            # Try multiple matching strategies
            if (normalized_data.lower() in normalized_scraped.lower() or 
                normalized_scraped.lower() in normalized_data.lower() or
                any(word in normalized_scraped.lower() for word in normalized_data.lower().split() if len(word) > 3)):
                
                # Avoid duplicates
                if uni_data not in matched_universities:
                    matched_universities.append(uni_data)
                    found = True
                    print(f"Matched: '{normalized_scraped}' -> '{uni_data['name']}'")
                    break
        
        # If no match found with existing data, create a basic entry for valid university names
        if not found and len(normalized_scraped) > 5 and ('university' in normalized_scraped.lower() or 'college' in normalized_scraped.lower()):
            basic_uni = {
                "name": normalized_scraped,
                "aLevels": "Check university website",
                "ib": "Check university website", 
                "admissionTest": "None",
                "fees": "Check university website",
                "location": "UK",
                "language": "Check university website"
            }
            matched_universities.append(basic_uni)
            print(f"Added basic entry for: '{normalized_scraped}'")
    
    return matched_universities

def generate_university_json():
    """Generate the universities JSON file"""
    try:
        print("Starting university data scraping...")
        matched_universities = match_universities_with_data()
        
        print(f"Successfully matched {len(matched_universities)} universities")
        
        if not matched_universities:
            print("No universities matched. Using fallback data...")
            # Fallback: use first 50 universities from our data
            matched_universities = universities_data[:50]
        
        # Save to JSON file
        with open("universities.json", "w", encoding="utf-8") as f:
            json.dump(matched_universities, f, indent=2, ensure_ascii=False)
        
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