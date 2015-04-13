use ciao;

select * from review limit 50;

insert into review
select * from review_bhagat;

insert into review
select * from review_vamshi;

insert into review
select * from review_uday;

insert into review
select * from review_rajesh;

select * from review limit 500;

select product_id, count(review_id)
from review
group by product_id
order by 2 desc;

select * from review limit 50;

select user_id, count(review_id)
from review
group by user_id
having count(review_id)>500
order by 2 ;

select * from product limit 500;


use ciao;

SET SQL_SAFE_UPDATES = 0;

# delete FROM `product` WHERE product_category = 'Shopping' or product_category ='Food & Drink' or product_category = 'Health' or product_category ='Education & Careers' or product_category = 'Ciao Café' or product_category ='House & Garden' or product_category = 'Fashion' or product_category ='Finance' or product_category ='Family';

select count(1) from product;

insert into review
select * from review_dump;

select count(1) from review_dump; # 179259

select count(1) from review;

insert into review
select * from review_dump
where product_id in (select prod_id from product); # 69943 rows deleted

select * from product limit 5;

use ciao;

delete from review;

select count(1) from review_dump;

use ciao;

select count(1) from product; # 70341

# SET SQL_SAFE_UPDATES = 0;

/*
delete
# select count(1)
from product
where product_subcategory in (
'Sky Travel',
'UK Horizons',
'TV Service Providers',
'Spas & Beauty Clinics',
'Muscle Stimulation Equipment',
'Cycling & Rowing Machines',
'Nutrition & Fitness',
'Other Kitchen Gadgets',
'Money & Competitions',
'Art & Culture',
'Health, Family & Lifestyle',
'Entertainment & Media',
'Computers & Internet',
'News & Current Affairs',
'Travel & Weather',
'Food & Drink',
'Motor Insurance Companies',
'Motoring Issues',
'Breakdown Organisations',
'Car Dealers',
'Car Importers',
'Car Supermarkets',
'Alfa Romeo',
'Audi',
'Comedy',
'Horror',
'Photo Developing',
'Networks & Tariffs',
'Turntables',
'Online Shopping',
'Web Services',
'Applications',
'Operating Systems',
'TV Series',
'Authors',
'Plays',
'Poetry',
'Thriller & Mystery',
'Science Fiction & Fantasy',
'Drama',
'Action & Adventure',
'Rock & Pop',
'Martial Arts',
'Jazz & Blues',
'World Cinema',
'Family',
'Musicals & Music Films',
'Documentaries & Biographies',
'Sports',
'War',
'Westerns',
'Teen',
'Music, TV & Movies',
'Celebrity Gossip',
'Literary',
'Hardcore, Punk & Heavy Metal',
'House, R&B;, Soul & Rap',
'Electronic',
'Classical',
'Easy Listening',
'Folk & Country',
'Reggae & Ska',
'World',
'Oldies',
'Soundtracks & Musicals',
'DJ Decks',
'Effects Pedals',
'Keyboards & Synthesizers',
'Newspapers',
'Local Radio stations',
'Nationwide Radio Stations',
'Breakfast Shows',
'Factual',
'Music',
'Sport',
'Talk',
'General',
'Charities',
'Theme Parks & Leisure Activites',
'Insurance Car',
'Solicitors & Accountants',
'Mobile Phone Networks',
'Magazines General',
'Newspapers-Daily',
'Fastfood & Chain Restaurants',
'Miscellaneous Services',
'Opticians',
'Supermarket & Chain Grocers',
'Holiday Camps',
'Children',
'Comedy / Drama',
'Film Channels',
'Lifestyle / Entertainment',
'Music Channels',
'News / Current Affairs',
'Sports Channels',
'Terrestrial',
'BBC1',
'ITV',
'MTV',
'Nickelodeon',
'BBC2',
'Cartoon Network',
'Channel 4',
'Channel 5',
'Fox Kids Network',
'ITV2',
'Sky 1',
'Living',
'BBC America',
'BBC Prime',
'Paramount Comedy Channel',
'UK Gold',
'Granada Plus',
'Hallmark',
'Sci-Fi',
'UK Style',
'Animal Planet',
'BBC Parliament',
'British Eurosport',
'Sky Sports 1',
'Other Car Manufacturers',
'Motoring Websites',
'Motoring Publications',
'Brakes V',
'Hair Medical Treatment',
'Bath Spas',
'Driving Schools',
'News & Politics',
'Science & Technology',
'Alternate History Books',
'Ciao Competitions',
'Categories',
'Member advice on...',
'Rewards at Ciao',
'Community Page & Cafe',
'Tenpin Bowling',
'Challenge TV',
'Muds & Masks',
'Photography',
'Kids',
'Comics',
'Motoring Magazines',
'Anime',
'Special Interest',
'Pickles, Salad Dressings, Relishes',
'Inline Skating',
'Other',
'Ciao Surveys',
'Ciao Features',
'Scuba BCDs',
'Audio Books',
'Business & Finance',
'Education & Careers',
'UK Hairdressers',
'Car Maintenance',
'Bravo',
'Hubs',
'Health Grills',
'Table Football',
'Business, Finance & Economy',
'Car Security',
'Royal Mail & Post Office',
'Bottom Brackets',
'Warranty Companies',
'Scuba Fins',
'False Nails',
'Insect Repellent',
'Comic Relief',
'Genealogy & Family Trees',
'Games',
'Blank Recording Media',
'Software Literature',
'Dodge',
'Health & Sliming Clubs',
'Pet Magazines',
'Paintball',
'Strategy Guides',
'Sky/Cable/Digital',
'Women Underwear & Lingerie',
'Scales',
'Waxing Equipment',
'Tea Makers',
'Health Monitors',
'Camera Film',
'GPS Software',
'Renault Scénic',
'Massage Therapy',
'Motorbike Maintenance',
'Gospel Music',
'Landline Service Providers',
'Choppers',
'Navigation',
'Outdoor Clothing',
'Economics Books',
'Crimpers',
'Harnesses',
'Belays',
'Crampons',
'Axes',
'Kitesurfing',
'Chevrolet',
'Cars & Motoring',
'Electrolysis'
) ; # 44314
*/



select count(1) from userinfo