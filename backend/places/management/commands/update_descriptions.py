import json
import os
from django.core.management.base import BaseCommand
from places.models import Place
from django.conf import settings

class Command(BaseCommand):
    help = 'Update place descriptions in DB and JSON file'

    def handle(self, *args, **options):
        # Map of Name -> Description
        descriptions = {
            "Swayambhunath": "Swayambhunath is an ancient religious architecture atop a hill in the Kathmandu Valley, west of Kathmandu city. It is also known as the Monkey Temple as there are holy monkeys living in the north-west parts of the temple.",
            "Boudhanath Stupa": "Boudhanath is a stupa in Kathmandu, Nepal. It is known as Khasti in Nepal Bhasa, Jyarung Khasyor in Tamang language. Located about 11 km from the center and northeastern outskirts of Kathmandu, the stupa's massive mandala makes it one of the largest spherical stupas in the world.",
            "Pashupatinath Temple": "The Pashupatinath Temple is a famous and sacred Hindu temple complex that is located on the banks of the Bagmati River, approximately 5 kilometres north-east of Kathmandu in the eastern part of Kathmandu Valley, the capital of Nepal.",
            "Kathmandu Durbar Square": "Kathmandu Durbar Square is one of three Durbar Squares in the Kathmandu Valley in Nepal that are UNESCO World Heritage Sites. Most of Kathmandu Durbar Square's fifty-plus monuments date from the 17th and 18th centuries.",
            "Patan Durbar Square": "Patan Durbar Square is situated at the centre of the city of Lalitpur in Nepal. It is one of the three Durbar Squares in the Kathmandu Valley which are UNESCO World Heritage Sites. One of its attractions is the ancient royal palace where the Malla Kings of Lalitpur resided.",
            "Bhaktapur Durbar Square": "Bhaktapur Durbar Square is the plaza in front of the royal palace of the old Bhaktapur Kingdom, 1400m above sea level. It is a UNESCO World Heritage Site. The Bhaktapur Durbar Square is located in the current town of Bhaktapur.",
            "Changu Narayan Temple": "The ancient Hindu temple of Changu Narayan is located on a high hilltop that is also known as Changu or Dolagiri. The temple was surrounded by forest with champak tree and a small village known as Changu. The temple is located in Changunarayan Municipality of Bhaktapur District, Nepal.",
            "Nagarkot": "Nagarkot is a village in central Nepal, at the rim of the Kathmandu Valley. It’s known for its views of the Himalayas, including Mount Everest to the northeast, which are especially striking at sunrise and sunset.",
            "Dhulikhel": "Dhulikhel is a municipality in Kavrepalanchok District of Nepal. Two major highway B.P. Highway and Araniko Highway passes through Dhulikhel. Araniko Highway connects Kathmandu, Nepal's capital city with Tibet's border town of Kodari.",
            "Chandragiri Hills": "Chandragiri Hill is seven kilometres from Thankot, and lies on the south-west side of Kathmandu Valley which is 2551 metres above sea level. The hill provides panoramic views of Kathmandu Valley and the Himalayan ranges from Annapurna to Everest.",
            "Pokhara Lakeside": "Lakeside is a popular tourist area in Pokhara, Nepal, located along the shores of Phewa Lake. It is known for its vibrant atmosphere, with numerous hotels, restaurants, bars, and shops catering to tourists.",
            "Phewa Lake": "Phewa Lake, Phewa Tal or Fewa Lake is a freshwater lake in Nepal formerly called Baidam Tal located in the south of the Pokhara Valley that includes Pokhara city; parts of Sarangkot and Kaskikot.",
            "Sarangkot": "Sarangkot is a ward of Pokhara in Kaski District, Nepal. It is a popular tourist destination for its sunrise and sunset views of the Annapurna range and for paragliding.",
            "Davis Falls": "Davis Falls is a waterfall located at Pokhara in Kaski District, Nepal. An underground tunnel conducts water from the fall. It is close to the Gupteshwar Mahadev Cave.",
            "Gupteshwor Mahadev Cave": "Gupteshwor Mahadev Cave is a cave located in Pokhara-17, Chhorepatan, Kaski district, Nepal. A cave is said to be 599.4 meters long. It is a major attraction of Pokhara.",
            "World Peace Pagoda": "Shanti Stupa is a Buddhist pagoda-style monument on Anadu Hill of the former Pumdi Bhumdi Village Development Committee, in the district of Kaski, Nepal.",
            "Begnas Lake": "Begnas Lake is a freshwater lake in Pokhara Metropolis of Kaski district of Nepal located in the south-east of the Pokhara Valley. The lake is the third largest lake of Nepal and second largest, after Phewa Lake, among the eight lakes in Pokhara Valley.",
            "Rupa Lake": "Rupa Lake or Rupa Tal is a freshwater lake in Nepal located in the border of Pokhara Metropolitan and Rupa Rural Municipality of Kaski District.",
            "International Mountain Museum": "The International Mountain Museum is a museum located in Pokhara, Nepal. It is dedicated to the mountains of Nepal, the mountaineers who climbed them and the people who live in them.",
            "Bindhyabasini Temple": "The Bindhyabasini Temple is one of the oldest temples in the city of Pokhara, Nepal. It is located in ward no. 2, Miruwa. It regularly attracts a large number of locals, Nepalis from across the country and foreigners alike.",
            "Lumbini": "Lumbini is a specialized Buddhist pilgrimage site in the Rupandehi District of Lumbini Province in Nepal. It is the place where, according to Buddhist tradition, Queen Mahamayadevi gave birth to Siddhartha Gautama at around 563 BCE.",
            "Maya Devi Temple": "The Maya Devi Temple is an ancient Buddhist temple situated at the UNESCO World Heritage Site of Lumbini, Nepal. It is the main temple at Lumbini, a site traditionally considered the birthplace of Gautama Buddha.",
            "Ashoka Pillar": "The Ashoka Pillar in Lumbini is one of the 3rd-century stone pillars built under the reign of the Mauryan emperor Ashoka. It was erected as a mark of respect by Ashoka after he visited Lord Buddha's place of birth and decided to accept Buddhism.",
            "World Peace Pagoda Lumbini": "The World Peace Pagoda, also called the Japan Peace Stupa, is a 21st-century monument in Lumbini, Nepal. It was built by Nipponzan-Myōhōji-Daisanga, a Japanese Buddhist order.",
            "Manimukunda Sen Park": "Manimukunda Sen Park, also known as Phulbari, is a park and historical site in Butwal, Nepal. It houses the ruins of the palace of King Manimukunda Sen of Palpa.",
            "Siddha Baba Temple": "Siddha Baba Temple is a Hindu temple dedicated to Lord Shiva located in Dobhan, Palpa district, near Butwal, Nepal. It is a popular pilgrimage site for devotees.",
            "Hill Park": "Hill Park is a popular recreational area in Butwal, offering panoramic views of the city and the surrounding terrain. It is a great spot for hiking and picnics.",
            "Banbatika Park": "Banbatika Park, or Shankarnagar Ban Bihar and Research Centre, is a large forest park and zoo in Tilottama, near Butwal. It features a zoo, picnic spots, and a children's park.",
            "ZipFlyer Nepal": "ZipFlyer Nepal offers one of the world's steepest and tallest ziplines. Located in Sarangkot, Pokhara, it provides an adrenaline-pumping experience with breathtaking views of the Annapurna range.",
            "Sarangkot Paragliding Pvt. Ltd": "Sarangkot Paragliding offers tandem paragliding flights from Sarangkot, Pokhara. It is one of the best ways to experience flight while enjoying views of Phewa Lake and the Himalayas.",
            "Annapurna Base Camp Trek": "The Annapurna Base Camp Trek is a popular trekking route in the Annapurna Conservation Area. It takes trekkers to the base of Mount Annapurna I, offering stunning mountain scenery and diverse landscapes.",
            "Poon Hill Trek": "Poon Hill is a hill station overlooking the Annapurna Massif range and Dhaulagiri mountain range, located on the border of Myagdi District and Kaski District in Gandaki Province of Nepal.",
            "Mardi Himal Trek": "The Mardi Himal Trek is a shorter, quieter trek in the Annapurna region. It offers spectacular close-up views of Mardi Himal and Machapuchare (Fishtail) mountain.",
            "Langtang Valley Trek": "The Langtang Valley Trek is known as the 'Valley of Glaciers'. It is a beautiful trek north of Kathmandu, offering views of Langtang Lirung and opportunities to experience Tamang culture.",
            "Chitwan National Park": "Chitwan National Park is the first national park in Nepal. It was established in 1973 and granted World Heritage Site status in 1984. It covers an area of 952.63 km and is located in the subtropical Inner Terai lowlands of south-central Nepal.",
            "Bardiya National Park": "Bardiya National Park is a protected area in Nepal that was established in 1988 as Royal Bardia National Park. Covering an area of 968 km it is the largest and most undisturbed national park in Nepal's Terai, adjoining the eastern bank of the Karnali River and bisected by the Babai River in the Bardiya District.",
            "Rara Lake": "Rara Lake is the biggest and deepest fresh water lake in the Nepal Himalayas. It is the main feature of Rara National Park, located in Jumla and Mugu Districts.",
            "Tilicho Lake": "Tilicho Lake is a lake located in the Manang district of Nepal, 55 kilometres as the crow flies from the city of Pokhara. It is situated at an altitude of 4,919 metres in the Annapurna range of the Himalayas.",
            "Gosaikunda": "Gosaikunda is an alpine freshwater oligotrophic lake in Nepal's Langtang National Park, located at an altitude of 4,380 m in the Rasuwa District with a surface of 13.8 ha.",
            "Kalinchowk": "Kalinchowk Bhagwati Temple is a Hindu shrine in Dolakha District of Nepal. It is situated in Kalinchowk VDC in Dolakha at the altitude of 3842m from sea level.",
            "Pathibhara Devi Temple": "Pathibhara Devi Temple or Mukkumlung is one of the most significant Hindu temples in Nepal, located on the hill of Taplejung. It is also considered one of the holy places for the Kirat people.",
            "Muktinath Temple": "Muktinath is a Vishnu temple, sacred to both Hindus and Buddhists. It is located in Muktinath Valley at the foot of the Thorong La mountain pass in Mustang, Nepal.",
            "Manakamana Temple": "The Manakamana Temple situated in the Gorkha district of Nepal is the sacred place of the Hindu Goddess Bhagwati, an incarnation of Parvati. The name Manakamana originates from two words, “mana” meaning heart and “kamana” meaning wish.",
            "Lumbini Museum": "The Lumbini Museum displays artifacts and historical items related to Buddhism and the Site of Lumbini. It provides insight into the history and archaeology of the region.",
            "Central Zoo": "The Central Zoo is a 6-hectare zoo in Jawalakhel, Nepal. It is the only zoo in Nepal and houses a variety of animals, birds, and reptiles.",
            "Kirtipur": "Kirtipur is an ancient city of Nepal. It is located in the Kathmandu Valley, 5 km southwest of the city of Kathmandu. It is known for its Newar culture, temples, and traditional architecture.",
            "Phulchowki": "Phulchowki is the highest hill surrounding the Kathmandu Valley, standing at 2782 meters. It is a popular destination for hiking, bird watching, and viewing snowfall in winter.",
            "Shivapuri Nagarjun National Park": "Shivapuri Nagarjun National Park is the ninth national park in Nepal and was established in 2002. It is located in the country's mid-hills on the northern fringe of the Kathmandu Valley.",
             "Thamel": "Thamel is a commercial neighborhood in Kathmandu, the capital of Nepal. It has been the centre of the tourist industry in Kathmandu for over four decades, starting from the hippie days when many artists came to Nepal and spent weeks in Thamel.",
             "Asan Tole": "Asan is a ceremonial, market, and residential square in central Kathmandu, the capital of Nepal. It is one of the most well-known historical locations in the city and is famed for its bazaar, festival calendar, and strategic location.",
             "Garden of Dreams": "The Garden of Dreams is a neo-classical garden in Kaiser Mahal, Kathmandu, Nepal, built in 1920. Designed by Kishore Narshingh, it consists of 6,895 square metres of gardens with three pavilions, an amphitheater, ponds, pergolas, and urns.",
             "Narayanhiti Palace Museum": "Narayanhiti Palace Museum is a public museum in Kathmandu, Nepal located east of the Kaiser Mahal and west of Yak and Yeti Hotel. The museum was the former royal palace in Kathmandu, of the Kingdom of Nepal.",
             "Hanuman Dhoka": "Hanuman Dhoka is a complex of structures with the Royal Palace of the Malla kings and also of the Shah dynasty in the Durbar Square of central Kathmandu, Nepal.",
             "Kumari Ghar": "Kumari Ghar is the palace in the center of Kathmandu Durbar Square where the Living Goddess Kumari resides. It is a beautiful example of traditional Newari architecture.",
             "Seti River Gorge": "The Seti River Gorge is a deep, narrow gorge carved by the Seti River in Pokhara. The milky white waters of the river rush through the gorge, which can be viewed from Mahendra Pul and other bridges.",
             "Mahendra Cave": "Mahendra Cave is a cave located in Pokhara-16, Batulechaur, Kaski district, Nepal. It is a large limestone cave containing stalactites and stalagmites.",
             "Bat Cave": "The Bat Cave, or Chamero Gufa, is a solutional cave located in Kaski District, Nepal. It is known for the thousands of bats that inhabit its dark chambers.",
             "Gorkha Durbar": "Gorkha Durbar involves a palace, a temple and a fort. It is a significant historical site located in Gorkha district, capturing the history of the Shah dynasty and the unification of Nepal.",
             "Bandipur": "Bandipur is a hilltop settlement and a municipality in Tanahun District, (Gandaki Province) of Nepal. Because of its preserved, old time cultural atmosphere, Bandipur has increasingly been coming to the attention of tourism.",
             "Ilam": "Ilam is a municipality and the tea producing town in Nepal. It is famous for its tea gardens, landscapes, and pleasant climate.",
             "Janakpur Dham": "Janakpur is a sub-metropolitan city in Dhanusha District, Madhesh Province, Nepal. It is a hub for religious and cultural tourism and is believed to be the birthplace of Goddess Sita.",
             "Janaki Mandir": "The Janaki Mandir is a Hindu temple in Janakpur, Nepal, dedicated to the Hindu goddess Sita. It is an example of ancient Rajput architecture and is an important pilgrimage site.",
             "Koshi Tappu Wildlife Reserve": "Koshi Tappu Wildlife Reserve is a protected area in the Terai of eastern Nepal covering 175 km of wetlands in the Sunsari, Saptari and Udayapur Districts.",
             "Sagarmatha National Park": "Sagarmatha National Park is a protected area in the Himalayas of eastern Nepal that is dominated by Mount Everest. It encompasses an area of 1,148 km in the Solukhumbu District.",
             "Tengboche Monastery": "Tengboche Monastery, also known as Dawa Choling Gompa, is a Tibetan Buddhist monastery of the Sherpa community. It is situated at 3,867 metres in the Khumbu region of eastern Nepal.",
             "Namche Bazaar": "Namche Bazaar is a town in Khumbu Pasanglhamu Rural Municipality in Solukhumbu District of Province No. 1 of north-eastern Nepal. It is the gateway to the high Himalayas and Mount Everest.",
             "Lukla": "Lukla is a small town in the Khumbu Pasanglhamu rural municipality of the Solukhumbu District in Province No. 1 of north-eastern Nepal. It is situated at 2,860 metres and is famous for its airport.",
             "Butwal City": "Butwal is a sub-metropolitan city in Rupandehi District in Lumbini Province of Nepal. It is a major connecting city for the hilly region and the Terai plains.",
             "Siddhartha Cable Car": "Siddhartha Cable Car is a cable car service in Butwal connecting the city to the historic Nuwakot Gadhi. It offers scenic views of Butwal and the surrounding hills.",
             "Lumbini Cable Car Station": "Lumbini Cable Car connects Butwal to Basantapur in Palpa. It is a new attraction offering panoramic views and access to the Kamhyakhya Temple.",
             "Red Sun Fun Park": "Red Sun Fun Park is a recreational park in Butwal offering various rides, swimming pools, and entertainment options for families and children.",
             "Tinau River": "The Tinau River is a Class II river in Nepal. It flows through Butwal and is a popular spot for relaxation and picnics along its banks.",
             "Amoosement Park": "Amoosement Park is a popular fun park in Butwal featuring water slides, swimming pools, and amusement rides.",
             "Global Peace Park": "Global Peace Park in Butwal is a peaceful green space dedicated to world peace. It features statues, gardens, and walking paths.",
             "Ostrich Farm": "The Ostrich Farm in Gangoliya, Rupandehi, near Butwal, is the largest ostrich farm in Nepal. Visitors can see ostriches and try ostrich meat dishes.",
             "Gajedi Taal": "Gajedi Taal is a lake located in the countryside near Butwal. It is a quiet spot for boating and picnicking, surrounded by forests.",
             "Kaparkatti Taal": "Kaparkatti Taal is a scenic lake near Butwal, known for its tranquil environment and boating facilities.",
             "BUTWAL CITY VIEW POINT NUWAKOT": "A scenic viewpoint in Nuwakot, Palpa, accessible from Butwal. It offers breathtaking night and day views of Butwal city and the Terai plains.",
             "Butwal Water Park and Resort Pvt. Ltd.": "A leisure destination in Butwal featuring water slides, swimming pools, and resort facilities for a fun-filled day out.",
             "Champadevi Hike": "Champadevi is a popular day hiking destination near Kathmandu. The trail passes through pine forests and offers panoramic views of the Kathmandu Valley and Himalayan ranges.",
             "Ultralight Flight Pokhara": "Ultralight flights in Pokhara offer a unique bird's-eye view of the Pokhara Valley, Phewa Lake, and the Annapurna mountains.",
             "Palpa Zipline, पाल्पा जिपलाइन": "Located near Butwal in Palpa district, this zipline offers an adventure experience with scenic views of the hills and forests.",
             "The Skate & Karts Zone": "An entertainment center in Butwal offering roller skating and go-karting facilities for fun and recreation.",
             "Paddle Nepal": "Paddle Nepal offers whitewater rafting and kayaking adventures on various rivers in Nepal, based out of Pokhara.",
             "Kathmandu Sport Climbing Center": "The Kathmandu Sport Climbing Center offers indoor rock climbing facilities for beginners and experienced climbers.",
             "Sainamaina Spring Water World and Resort": "A resort and water park located in Sainamaina, near Butwal, utilizing natural spring water for its pools.",
             "Sundarijal Waterfall(Chisapani Trek)": "Sundarijal is a major water source for Kathmandu and the starting point for the Chisapani trek. The waterfalls and Shivapuri National Park entrance are key attractions.",
             "Hide Out Restro": "A popular restaurant in Butwal known for its ambiance and variety of food options.",
             "the wonderland funpark": "A fun park in Kathmandu offering various rides and entertainment for children and families.",
             "El Dorado Avenue": "A dining and recreational venue in Butwal.",
             "Cloud 9 Cafe क्लाउड नाइन क्याफे": "A cafe in Butwal offering coffee, drinks, and a place to hang out.",
             "Manjushree Park(zipline)": "Located near Chobhar Gorge in Kathmandu, Manjushree Park features a zipline and cave exploration opportunities, along with scenic views.",
             "36 Riverside": "A restaurant or resort located by the riverside in Butwal, offering a pleasant outdoor setting.",
             "Cravings": "A restaurant in Butwal known for its delicious food and diverse menu.",
             "the beans & bar ‘द’": "A cafe and bar in Butwal, a popular spot for socializing and enjoying drinks.",
             "The Lavish Lounge and Bar": "A lounge and bar in Butwal offering a premium nightlife experience.",
             "Good DO , The Vegan Kitchen": "A vegan restaurant in Butwal offering plant-based meals and healthy options.",
             "Soulmate Restaurant Butwal": "A restaurant in Butwal known for its hospitality and good food.",
             "Trishuli River Rafting Nepal": "Rafting on the Trishuli River is one of the most popular river rafting adventures in Nepal, easily accessible from Kathmandu and Pokhara.",
             "The Garden Cafe And Restaurant": "A cafe and restaurant in Butwal with a garden setting for a relaxed dining experience.",
             "Daddy's Kitchen The cafe and Restaurant": "A family-friendly restaurant in Butwal offering a variety of cuisines.",
             "Grassland Nepal": "A venue or resort in Butwal, likely offering open spaces and recreational activities.",
             "Upper Bhotekoshi Rafting": "Upper Bhotekoshi Rafting offers steep and technical whitewater rafting for adventure seekers.",
             "Karlo Restaurant and Bar": "A restaurant and bar in Butwal.",
             "The Coffee Club, Butwal": "A coffee shop in Butwal serving fresh coffee and snacks.",
             "Bhojan Griha": "Bhojan Griha is a traditional Nepali restaurant in Kathmandu housed in a historic building, serving authentic Nepali cuisine with cultural shows.",
             "Nirvana Restaurant & Bar": "A restaurant and bar in Butwal.",
             "Cafe de hungry": "A cafe in Butwal.",
             "URBAN STREET Restaurant & Bar": "A restaurant and bar in Butwal offering a modern dining experience.",
             "Cafe de Patan": "A cafe located in Patan, offering a cozy atmosphere and good food.",
             "Cafe gossip": "A cafe in Butwal.",
             "Cafe Soma": "A popular cafe in Kathmandu known for its breakfast and brunch menu.",
             "Nectar Bonanza": "A venue in Butwal, possibly a restaurant or juice bar.",
             "Moondance Restaurant": "A well-known restaurant in Pokhara Lakeside, famous for its lemon meringue pie and diverse menu.",
             "Gaule Chulo": "A restaurant in Butwal serving traditional Nepali countryside style food.",
             "Dough Bakery And Cafe": "A bakery and cafe in Kathmandu known for its pastries and coffee.",
             "Fresh Elements Café": "A cafe in Pokhara offering healthy and fresh food options.",
             "Fire and Ice Restaurant": "A branch or intended name similar to the famous Kathmandu pizzeria, likely located in Butwal or mislabeled, but generally refers to a pizza place.",
             "Mini lake Butwal": "A man-made or natural small lake area in Butwal developed for tourism and recreation.",
             "Caffe Concerto": "A popular Italian restaurant and cafe in Pokhara.",
             "Himalayan Java Coffee": "The first specialty coffee chain in Nepal, with a branch in Kathmandu offering premium Nepal-grown coffee.",
             "Pathik Foundation-Rupandehi": "A foundation or center in Rupandehi, likely involved in social work or community activities.",
             "OR2K Pokhara": "The Pokhara branch of the famous vegetarian restaurant OR2K, offering Israeli and Middle Eastern cuisine.",
             "Mokshya Yoga & Fitness": "A yoga and fitness studio in Butwal.",
             "Nanglo Thakali Bhancha Ghar": "A restaurant in Pokhara specializing in Thakali cuisine, a traditional food from the Mustang region.",
             "Bliss Yoga & Wellness Center": "A wellness center in Butwal offering yoga and holistic health services.",
             "Shree Siddhababa Temple": "A temple dedicated to Siddhababa.",
             "Duna tapari mo mo House": "A restaurant in Pokhara specializing in Momo (Nepalese dumplings) served in leaf plates (Duna Tapari).",
             "Le Sherpa Restaurant": "A fine dining restaurant in Kathmandu offering European cuisine and a beautiful outdoor seating area.",
             "Shree Durga Bhagawati Mandir": "A Hindu temple dedicated to Goddess Durga in Butwal.",
             "Fewa Lake Phokhara": "Phewa Lake is the second largest lake in Nepal and the center of attraction in Pokhara. Visitors can enjoy boating and the reflection of Mount Machhapuchhre.",
             "Radha Krishna Temple (राधा कृष्ण मन्दिर )": "A temple dedicated to Lord Krishna and Radha in Butwal.",
             "नीलकण्ठ बाबा धाम": "A religious site in Butwal dedicated to Shiva (Nilkantha).",
             "Chiya Moksha": "A tea house or cafe in Kathmandu.",
             "Shree Siddeswar Shiva Mandir": "A Shiva temple in Butwal.",
             "श्री महावीर हनुमानगढी मन्दिर": "A Hanuman temple in Butwal.",
             "Pokhara Cineplex": "A movie theater in Pokhara.",
             "Newa Lahana": "A community-run restaurant in Kirtipur serving authentic Newari cuisine.",
             "OR2K": "A popular vegetarian restaurant in Kathmandu known for its Middle Eastern platters and relaxed atmosphere.",
             "Pumpernickel Bakery": "A long-standing bakery in Thamel, Kathmandu, famous for its yak cheese sandwiches and pastries.",
             "Sarangkot Viewpoint": "The viewpoint tower at Sarangkot offering the widest panoramic views of the Himalayas.",
             "Roadhouse Cafe": "A popular restaurant chain in Kathmandu known for its wood-fired pizzas and coffee.",
             "Thakali Bhanchha Ghar": "A restaurant in Kathmandu specializing in authentic Thakali trekking food.",
             "The Bakery Café": "One of the oldest bakery cafe chains in Kathmandu, employing many hearing-impaired staff.",
             "Third Eye Restaurant & Café": "A well-established Indian and continental restaurant in Thamel, Kathmandu.",
             "Bouddhanath": "Boudhanath Stupa is one of the largest spherical stupas in the world and a center of Tibetan Buddhism in Nepal.",
             "Fairfield Central Shopping Centre": "A shopping center in Pokhara.",
             "Pokhara Old Bazaar": "The traditional market area of Pokhara with old Newari architecture and temples.",
             "Himalayan Yoga Academy": "A yoga school in Kathmandu offering teacher training and retreats.",
             "Potala Tibetan Shop": "A shop in Pokhara selling Tibetan handicrafts and souvenirs.",
             "Kamal Pokhari": "A historic pond in Kathmandu, recently restored as a park.",
             "Pokhara Trade Mall": "A shopping mall in Pokhara.",
             "Kopan Monastery": "A Tibetan Buddhist monastery near Boudhanath, Kathmandu, famous for its meditation courses.",
             "Kunti Mall": "A shopping mall in Pokhara.",
             "Namobuddha Monastery": "Thrangu Tashi Yangtse Monastery is a Tibetan Buddhist monastery in Namobuddha, a sacred pilgrimage site.",
             "Butwal City Center": "A shopping or commercial center in Butwal.",
             "Singh Complex": "A commercial complex in Butwal.",
             "Bagmati Gandaki stores": "A store in Pokhara.",
             "Butwal Online Shopping Center": "An e-commerce or physical store in Butwal.",
             "B Town Streetwear": "A clothing store in Butwal.",
             "Yak & Yeti Clothing": "A clothing store in Pokhara.",
             "Ranibari Community Forest": "A protected forest area within Kathmandu city, offering walking trails and bird watching.",
             "Dwa Complex": "A commercial complex in Pokhara.",
             "Swambhunath": "Swayambhunath Stupa is an ancient religious complex atop a hill in the Kathmandu Valley.",
             "Yoga Life Studio": "A yoga studio in Kathmandu.",
             "Yogmandu Yoga": "A yoga studio in Kathmandu.",
             "99shop Butwal": "A budget shop in Butwal.",
             "Viva +99 Shopping Butwal": "A shopping outlet in Butwal.",
             "BG Mall": "A shopping mall in Gongabu, Kathmandu, with a cinema and food court.",
             "butwal bhatbhateni": "The Butwal branch of Bhat-Bhateni Supermarket.",
             "Plus Size Nepal Butwal Branch": "A clothing store for plus-size apparel in Butwal.",
             "Bhatbhateni Super Market": "The largest supermarket chain in Nepal, offering a wide range of products.",
             "Devi’s Fall": "Patale Chhango (David's Fall) is a waterfall where water vanishes into an underground passage.",
             "Srijana Street": "A street or commercial area in Butwal.",
             "CITY CENTRE": "A shopping mall in Kamal Pokhari, Kathmandu.",
             "Lumbini Furniture bazar": "A furniture market in Butwal.",
             "Civil Mall": "A shopping mall in Sundhara, Kathmandu.",
             "Le Fabec Butwal": "A restaurant or cafe in Butwal.",
             "Durbar Mall": "A luxury shopping mall in Durbarmarg, Kathmandu.",
             "NG Market": "A market or shopping area in Butwal.",
             "Labim Mall": "A premium shopping mall in Pulchowk, Lalitpur (Kathmandu Valley).",
             "Ib collection butwal": "A clothing or fashion collection store in Butwal.",
             "Rising Mall": "A shopping mall in Durbarmarg, Kathmandu.",
             "Satyawati Complex": "A commercial complex in Butwal.",
             "Best one Shop": "A shop in Butwal.",
             "Sherpa Mall": "A shopping mall in Durbarmarg, Kathmandu.",
             "Club Catwalk": "A nightclub in Pokhara.",
             "Rolling Stone Rock Bar": "A rock music bar in Pokhara (or Kathmandu).",
             "Tilottama Park": "A park in Tilottama municipality near Butwal.",
             "Paradiso Pokhara": "A sports bar and grill in Pokhara.",
             "Cozy Castle | Social Club and Bar": "A social club and bar in Butwal.",
             "Club Plan B": "A nightclub in Butwal.",
             "The Concept Club and Pub": "A club and pub in Butwal.",
             "Pasang Lhamu Sports Climbing Centre": "A sports climbing center named after Pasang Lhamu Sherpa, offering wall climbing facilities.",
             "Butwal skate park": "A skate park in Butwal for skateboarding enthusiasts.",
             "Bhoot Khola": "A natural pool with blue water located along the Butwal-Palpa road, popular for swimming and photos.",
             "Busy Bee Café": "A famous bar and cafe in Pokhara Lakeside with live music.",
             "Aqua Water Park Lumbini": "A water park resort in the Lumbini region.",
             "Lumbini Indoor Sports": "An indoor sports facility in Butwal.",
             "Butwal fulbari": "Manimukunda Sen Park, often referred to as Phulbari, is a historic garden and park in Butwal with palace ruins.",
             "Chandragiri Cable Car": "Chandragiri Cable Car is a gondola lift transportation system located in Chandragiri Municipality, Nepal. The cable car runs from Thankot to Chandragiri Hills, offering panoramic views of Kathmandu Valley.",
             "Cloud 9 Cafe क्लाउड नाइन क्याफ़े": "Cloud 9 Cafe is a popular hangout spot in Butwal, known for its cozy ambiance and variety of coffee and snacks.",
             "Kamal Pokhari": "Kamal Pokhari is a historic pond in Kathmandu (and also a landmark in Butwal), recently restored. It is known for its lotus flowers and serene environment.",
             "Kunja Park": "Kunja Park is a recreational park in Butwal, providing a green space for relaxation and family outings.",
             "Lake side": "Lakeside is a popular tourist area in Pokhara, Nepal, located along the shores of Phewa Lake. It is known for its vibrant atmosphere, with numerous hotels, restaurants, bars, and shops catering to tourists.",
             "Pharping Hike": "Pharping Hike takes you to the southern edge of Kathmandu Valley. It is a pilgrimage site with monasteries and temples, offering a mix of culture and nature.",
             "Shivpuri Nagarjuna National Park": "Shivapuri Nagarjun National Park is the ninth national park in Nepal, located on the northern fringe of the Kathmandu Valley, famous for its watershed and biodiversity.",
             "Tinau Waterpark and Party Palace Pvt. Ltd.": "Tinau Waterpark is a fun destination in Butwal featuring water slides and pools, perfect for cooling off in the summer."
         }
        
        # Load JSON file
        json_file_path = os.path.join(settings.BASE_DIR, 'all_149_places_updated.json')
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                places_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return

        updated_count = 0
        
        # Update JSON data and DB
        for place_item in places_data:
            name = place_item.get('name')
            if name in descriptions:
                new_desc = descriptions[name]
                
                # Update JSON object
                place_item['description'] = new_desc
                
                # Update Database
                try:
                    # Filter all matches (handling duplicates) and update all
                    places_qs = Place.objects.filter(name=name)
                    if places_qs.exists():
                        updated_rows = places_qs.update(description=new_desc)
                        updated_count += updated_rows
                        self.stdout.write(f"Updated {updated_rows} record(s) for: {name}")
                    else:
                        self.stdout.write(self.style.WARNING(f"Place not found in DB: {name}"))
                except Exception as e:
                     self.stdout.write(self.style.ERROR(f"Error updating DB for {name}: {e}"))
            else:
                self.stdout.write(self.style.WARNING(f"No description found for: {name}"))

        # Save updated JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(places_data, f, indent=2, ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} places in DB and saved to JSON file.'))
