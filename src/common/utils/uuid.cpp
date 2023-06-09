//
// Created by kingdo on 2022/3/5.
//
#include <df/utils/locks.h>
#include <df/utils/radom.h>
#include <df/utils/uuid.h>

static std::atomic_int counter       = 0;
static std::atomic_size_t gidKeyHash = 0;
static std::mutex mutex;

namespace df::utils
{
    uint32_t uuid()
    {
        df::utils::UniqueLock lock(mutex);

        std::mt19937_64 engine(std::random_device {}());
        std::uniform_int_distribution<uint32_t> distribution;

        return distribution(engine);
    }

    /// 说实话，这实现多少有点装神弄鬼
    //    uint32_t uuid()
    //    {
    //        if (gidKeyHash.load(std::memory_order_relaxed) == 0)
    //        {
    //            df::utils::UniqueLock lock(mutex);
    //            if (gidKeyHash == 0)
    //            {
    //                // Generate random hash
    //                std::string gidKey = df::utils::randomString(UUID_LEN);
    //                gidKeyHash         = std::hash<std::string> {}(gidKey);
    //            }
    //        }
    //
    //        uint32_t intHash = gidKeyHash.load(std::memory_order_relaxed) % UINT32_MAX;
    //        uint32_t result  = intHash + counter.fetch_add(1);
    //        if (result)
    //        {
    //            return result;
    //        }
    //        else
    //        {
    //            return intHash + counter.fetch_add(1);
    //        }
    //    }

    //    void uuid_reset()
    //    {
    //        counter    = 0;
    //        gidKeyHash = 0;
    //    }
}