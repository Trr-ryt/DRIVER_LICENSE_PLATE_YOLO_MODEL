class ThaiLicenseHelper:
    # Class-level constants for mappings
    CHARACTER_MAPPING = {
        "A01": "ก", "A02": "ข", "A04": "ค", "A06": "ฆ", "A07": "ง", "A08": "จ",
        "A09": "ฉ", "A10": "ช", "A12": "ฌ", "A13": "ญ", "A14": "ฎ", "A16": "ฐ",
        "A18": "ฒ", "A19": "ณ", "A20": "ด", "A21": "ต", "A22": "ถ", "A23": "ท",
        "A24": "ธ", "A25": "น", "A26": "บ", "A27": "ป", "A28": "ผ", "A30": "พ",
        "A31": "ฟ", "A32": "ภ", "A33": "ม", "A34": "ย", "A35": "ร", "A36": "ล",
        "A37": "ว", "A38": "ศ", "A39": "ษ", "A40": "ส", "A41": "ห", "A42": "ฬ",
        "A43": "อ", "A44": "ฮ",
    }

    PROVINCE_MAPPING = {
        "ACR": "อำนาจเจริญ", "ATG": "อ่างทอง", "AYA": "พระนครศรีอยุธยา",
        "BKK": "กรุงเทพมหานคร", "BKN": "บึงกาฬ", "BRM": "บุรีรัมย์",
        "BTG": "บางที", "CBI": "ชลบุรี", "CCO": "ฉะเชิงเทรา", "CMI": "เชียงใหม่",
        "CNT": "เชียงราย", "CPM": "ชัยภูมิ", "CPN": "ชุมพร", "CRI": "เชียงราย",
        "CTI": "จันทบุรี", "KBI": "กระบี่", "KKN": "ขอนแก่น", "KPT": "กำแพงเพชร",
        "KRI": "กาญจนบุรี", "KSN": "กาฬสินธุ์", "LEI": "เลย", "LPG": "ลำปาง",
        "LPN": "ลำพูน", "LRI": "ลพบุรี", "MDH": "มหาสารคาม", "MKM": "แม่ฮ่องสอน",
        "MSN": "แม่สอด", "NAN": "น่าน", "NBI": "นนทบุรี", "NBP": "นครปฐม",
        "NKI": "นครศรีธรรมราช", "NMA": "นครสวรรค์", "NPM": "นครพนม",
        "NPT": "นครปฐม", "NSN": "หนองคาย", "NST": "นครศรีธรรมราช",
        "NYK": "หนองคาย", "PBI": "เพชรบุรี", "PCT": "เพชรบูรณ์",
        "PKN": "ประจวบคีรีขันธ์", "PKT": "ภูเก็ต", "PLG": "พัทลุง",
        "PLK": "พิษณุโลก", "PNA": "พังงา", "PNB": "ปัตตานี", "PRE": "แพร่",
        "PRI": "ปราจีนบุรี", "PTE": "ปทุมธานี", "PTN": "ปัตตานี", "PYO": "พะเยา",
        "RBR": "ราชบุรี", "RET": "ร้อยเอ็ด", "RNG": "ระนอง", "RYG": "ระยอง",
        "SBR": "สิงห์บุรี", "SKA": "สงขลา", "SKM": "สมุทรสงคราม",
        "SKN": "สมุทรสาคร", "SKW": "สมุทรปราการ", "SNI": "สระแก้ว",
        "SNK": "สระบุรี", "SPB": "สุพรรณบุรี", "SPK": "สมุทรปราการ",
        "SRI": "ศรีสะเกษ", "SRN": "สุรินทร์", "SSK": "ศรีสะเกษ", "STI": "สตูล",
        "TAK": "ตาก", "TRG": "ตรัง", "TRT": "ตราด", "UBN": "อุบลราชธานี",
        "UDN": "อุดรธานี", "UTI": "อุตรดิตถ์", "UTT": "อุทัยธานี",
        "YLA": "ยะลา", "YST": "ยโสธร"
    }

    @staticmethod
    def get_thai_character(code):
        """Get the Thai character or province name for a given code."""
        return ThaiLicenseHelper.CHARACTER_MAPPING.get(code, ThaiLicenseHelper.PROVINCE_MAPPING.get(code, code))

    @staticmethod
    def split_license_plate_and_province(text):
        """Split the license plate and province from the given text."""
        # Find the last digit in the text
        last_number_index = len(text) - 1
        while last_number_index >= 0 and not text[last_number_index].isdigit():
            last_number_index -= 1

        if last_number_index >= 0:
            # Split into license plate and province
            license_plate = text[:last_number_index + 1]
            province = text[last_number_index + 1:]
            return license_plate, province
        return None, None
