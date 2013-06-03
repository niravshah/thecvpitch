require 'linkedin-scraper'
profile = Linkedin::Profile.get_profile("http://www.linkedin.com/in/elmervandenheuvel")
puts profile.current_companies
puts profile.past_companies
puts profile.skills
