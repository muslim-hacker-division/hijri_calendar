import datetime
import sys
from hijri_converter import Hijri, Gregorian

class HijriCalendar:
    def __init__(self):
        self.hijri_months = [
            "Muharram", "Safar", "Rabi'ul Awal", "Rabi'ul Akhir",
            "Jumadil Awal", "Jumadil Akhir", "Rajab", "Sya'ban",
            "Ramadhan", "Syawal", "Dzulqa'dah", "Dzulhijjah"
        ]
        
        self.day_names = [
            "Ahad", "Senin", "Selasa", "Rabu", 
            "Kamis", "Jumat", "Sabtu"
        ]
        
    def get_today_hijri(self):
        today = Gregorian.today()
        hijri = today.to_hijri()
        return f"{hijri.day} {self.hijri_months[hijri.month-1]} {hijri.year} H"
    
    def display_month(self, year=None, month=None):
        if year is None or month is None:
            hijri_today = Hijri.today()
            year = hijri_today.year
            month = hijri_today.month
        
        try:
            first_day = Hijri(year, month, 1)
            last_day = Hijri(year, month, first_day.month_length())
            
            print(f"\n{'='*60}")
            print(f"  {self.hijri_months[month-1]} {year} H")
            print(f"{'='*60}")
            
            # Print day names
            day_header = ""
            for day in self.day_names:
                day_header += f"{day:^8}"
            print(day_header)
            
            # Get starting weekday (0=Sunday, 1=Monday, etc.)
            start_weekday = first_day.day_week()
            
            # Print leading spaces
            print("   " * start_weekday, end="")
            
            # Print days
            for day in range(1, last_day.day + 1):
                hijri_date = Hijri(year, month, day)
                gregorian = hijri_date.to_gregorian()
                
                # Mark today
                today = Hijri.today()
                is_today = (hijri_date.year == today.year and 
                           hijri_date.month == today.month and 
                           hijri_date.day == today.day)
                
                day_str = f"{day:^7}"
                if is_today:
                    day_str = f"\033[91m{day_str}\033[0m"  # Red color for today
                
                print(day_str, end=" ")
                
                # New line after Saturday
                if (day + start_weekday) % 7 == 0:
                    print()
            
            print("\n")
            
            # Print footer with Gregorian equivalent
            greg_first = first_day.to_gregorian()
            greg_last = last_day.to_gregorian()
            print(f"Masehi: {greg_first.day} {greg_first.strftime('%B')} {greg_first.year} - {greg_last.day} {greg_last.strftime('%B')} {greg_last.year}")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def convert_date(self, gregorian_date):
        try:
            year, month, day = map(int, gregorian_date.split('-'))
            greg = Gregorian(year, month, day)
            hijri = greg.to_hijri()
            return f"{hijri.day} {self.hijri_months[hijri.month-1]} {hijri.year} H"
        except Exception as e:
            return f"Error: {e}"
    
    def run(self):
        print("\n=== HIJRI CALENDAR ===")
        print(f"Hari ini: {self.get_today_hijri()}")
        
        while True:
            print("\nMenu:")
            print("1. Lihat kalender bulan ini")
            print("2. Lihat kalender bulan tertentu")
            print("3. Konversi tanggal Masehi ke Hijriyah")
            print("4. Keluar")
            
            choice = input("Pilih menu (1-4): ")
            
            if choice == '1':
                self.display_month()
            elif choice == '2':
                try:
                    year = int(input("Tahun Hijriyah: "))
                    month = int(input("Bulan (1-12): "))
                    self.display_month(year, month)
                except ValueError:
                    print("Input tidak valid. Masukkan angka.")
            elif choice == '3':
                date_input = input("Masukkan tanggal Masehi (YYYY-MM-DD): ")
                result = self.convert_date(date_input)
                print(f"Tanggal Hijriyah: {result}")
            elif choice == '4':
                print("Terima kasih telah menggunakan Hijri Calendar!")
                break
            else:
                print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    calendar = HijriCalendar()
    calendar.run()