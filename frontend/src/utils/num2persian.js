export default function num2persian(input) {
    const ones = ['', 'یک', 'دو', 'سه', 'چهار', 'پنج', 'شش', 'هفت', 'هشت', 'نه'];
    const tens = ['', 'ده', 'بیست', 'سی', 'چهل', 'پنجاه', 'شصت', 'هفتاد', 'هشتاد', 'نود'];
    const hundreds = ['', 'صد', 'دویست', 'سیصد', 'چهارصد', 'پانصد', 'ششصد', 'هفتصد', 'هشتصد', 'نهصد'];
    const thousands = ['', 'هزار', 'میلیون', 'میلیارد'];

    if (isNaN(input)) return '';
    let num = parseInt(input, 10);
    if (num === 0) return 'صفر';

    let str = '';
    let k = 0;
    while (num > 0) {
        let part = num % 1000;
        if (part !== 0) {
            let partStr = '';
            let h = Math.floor(part / 100);
            let t = Math.floor((part % 100) / 10);
            let o = part % 10;
            if (h) partStr += hundreds[h] + ' و ';
            if (t > 1) {
                partStr += tens[t] + (o ? ' و ' + ones[o] : '');
            } else if (t === 1) {
                if (o === 0) partStr += 'ده';
                else if (o === 1) partStr += 'یازده';
                else if (o === 2) partStr += 'دوازده';
                else if (o === 3) partStr += 'سیزده';
                else if (o === 4) partStr += 'چهارده';
                else if (o === 5) partStr += 'پانزده';
                else if (o === 6) partStr += 'شانزده';
                else if (o === 7) partStr += 'هفده';
                else if (o === 8) partStr += 'هجده';
                else if (o === 9) partStr += 'نوزده';
            } else if (o) {
                partStr += ones[o];
            }
            partStr = partStr.replace(/ و $/, '');
            str = partStr + (thousands[k] ? ' ' + thousands[k] : '') + (str ? ' و ' + str : '');
        }
        num = Math.floor(num / 1000);
        k++;
    }
    return str.trim();
} 