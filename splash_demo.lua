function main(splash, args)

  -- spoof request header by setting name of user agent
  --[[
  -- Alternative 1: unwanted pop-up exists and
  -- you can only change user agent header
  splash:set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
  --]]
  
  --[[
  -- Alternative 2: set custom headers
  -- allow you to change other header elements
  headers = {
    ['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
  }
  
  splash:set_custom_headers(headers)
  --]]
  
  -- Alternative 3: 
  -- allow you to change other header elements
  splash:on_request(function(request)
    request:set_header('User-Agent',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
  end)
  
  url = args.url -- get the input url from args
  
  -- use assert to check if going to the url is valid 
  assert(splash:go(url)) 
  
  -- wait for some time for all javascript to 
  -- finish loading for certain js-heavy site
  assert(splash:wait(1))
  
  -- select the input using css-selector
  -- splash:select to select only one id element
  -- splash:select_all to select all elements
  input_box = assert(splash:select("#search_form_input_homepage"))
  
  -- input box has to be in focus state to fill in text
  input_box:focus()
  
  -- fill input box with text
  input_box:send_text("my user agent")
  
  --[[
  -- Alternative 1: click on search button
  -- to get result
  -- select the search button
  btn = assert(splash:select("#search_button_homepage"))
  btn:mouse_click()
  assert(splash:wait(1))
  
  -- wait for a moment
  assert(splash:wait(1))
  --]]
  
  -- Alternative 2: press enter to get result
  input_box:send_keys("<Enter>")
  assert(splash:wait(1))
  
  -- set viewport to full resolution
  splash:set_viewport_full()
  
  return {
    image = splash:png(),
    html = splash:html()
  }
end

https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/
