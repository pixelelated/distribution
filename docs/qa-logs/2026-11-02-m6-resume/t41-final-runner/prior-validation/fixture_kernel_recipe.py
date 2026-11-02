"""Synthetic line-number fixture only; no config sourcing."""
lines=['# synthetic filler']*54
entries={16:'PKG_PATCH_DIRS="mainline default"',18:'[[ "${DEVICE}" == RK* ]] && PKG_PATCH_DIRS+=" mainline-rockchip"',21:'case ${DEVICE} in',22:'  RK3588)',23:'    PKG_VERSION="'+('a'*40)+'"',27:'    PKG_PATCH_DIRS="device default"',29:'  H700|SM8550)',30:'    PKG_VERSION="7.2"',36:'  RK3326|GENERIC_X64)',37:'    PKG_VERSION="7.1.2"',40:'    PKG_PATCH_DIRS+=" 7.0"',42:'  RK3576|RK3566)',43:'    PKG_VERSION="7.0.2"',46:'    PKG_PATCH_DIRS+=" 7.0"',48:'  S922X|RK3399)',49:'    PKG_VERSION="6.18.49"',53:'esac'}
for n,line in entries.items():lines[n-1]=line
RECIPE='\n'.join(lines)+'\n'
PATH='projects/ROCKNIX/packages/linux/package.mk'
SOURCE='02aab33bd9842610b0d466c9c186454dc14373ee'
QUOTE=SOURCE+':'+PATH+'\n```text\n'+'\n'.join(str(n)+':'+lines[n-1] for n in [16,18,22,23,27,29,30,36,37,40,42,43,46,48,49])+'\n```\n'
