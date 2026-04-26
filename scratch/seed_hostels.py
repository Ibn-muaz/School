import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

from hostels.models import Hostel, Room, BedSpace

def seed_hostels():
    # Male Hostels
    m_hostel1, _ = Hostel.objects.get_or_create(
        name="Abubakar Sadiq Hall",
        gender_category='male',
        price_per_session=25000.00,
        description="Standard male hostel located in the Eastern Wing."
    )
    
    m_hostel2, _ = Hostel.objects.get_or_create(
        name="Benue Hall",
        gender_category='male',
        price_per_session=30000.00,
        description="Premium male hostel with en-suite facilities."
    )
    
    # Female Hostels
    f_hostel1, _ = Hostel.objects.get_or_create(
        name="Queen Amina Hall",
        gender_category='female',
        price_per_session=25000.00,
        description="Main female hostel near the College clinic."
    )
    
    f_hostel2, _ = Hostel.objects.get_or_create(
        name="Nana Asma'u Hall",
        gender_category='female',
        price_per_session=35000.00,
        description="Luxury female hostel with 24/7 power backup."
    )
    
    # Create Rooms and Beds for each
    for hostel in [m_hostel1, m_hostel2, f_hostel1, f_hostel2]:
        for i in range(1, 11): # 10 rooms each
            room, _ = Room.objects.get_or_create(
                hostel=hostel,
                room_number=f"{i:03d}",
                capacity=4
            )
            for char in ['A', 'B', 'C', 'D']:
                BedSpace.objects.get_or_create(
                    room=room,
                    bed_identifier=char,
                    is_available=True
                )
    print("Hostels, Rooms, and Bed Spaces seeded successfully!")

if __name__ == "__main__":
    seed_hostels()
