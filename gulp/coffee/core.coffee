((window, document, ProJ, $) ->
  'use strict'

# ----------------------------------------------------------------------------------------------------

  DEBUG = no

  jPro = new ProJ DEBUG, '/assets'
  window.jPro = window.$$ = jPro

  $win = $ window

  fnHeight = ->
    height = window.innerHeight
    $('.screen').each ->
      @style.height = ''
      @style.height = if $(@).outerHeight() < height then "#{ height }px" else ''
  $win.resize fnHeight
  fnHeight()

# --------------------------------------------------

  $ ->
    new WOW(offset: 0).init()

    jPro.lazy '[data-lazy]'

    $('a.active, .active > a').on 'click', (event) -> event.preventDefault()

    $('.totop').on 'click', jPro.totop
    $('.w3c').on 'click', jPro.w3c
    $('.ymet').on 'click', jPro.ymet

    $('#navbar .nav-link').on 'click', (event) ->
      event.preventDefault()
      jPro.toobj @getAttribute 'href' if not @classList.contains 'active'

    $('.panel .collapse').on 'shown.bs.collapse', -> jPro.toobj @parentNode, 40

    $('body').scrollspy
      target: '#navbar'
      offset: 50

    jPro.lightbox '[data-lightbox]'

    $autosize = $ '.autosize'
    jPro.script 'js/lib/jquery.autosize.js', -> $autosize.autosize() if $autosize.length

# --------------------------------------------------

  $win.load ->
    fnHeight()

# ----------------------------------------------------------------------------------------------------

) window, document, ProJ, jQuery
